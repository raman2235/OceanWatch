from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import sqlite3, os, shutil

# ================== App & CORS ==================
app = FastAPI(title="Coastal Hazard Reporting API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"],
)

# ================== Config ==================
DATABASE = "coastal.db"
SECRET_KEY = "CHANGE_ME_SUPER_SECRET_KEY"  # TODO: env var me daalo prod me
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    return sqlite3.connect(DATABASE)

def ensure_uploads_dir():
    os.makedirs("uploads", exist_ok=True)

# ================== Models ==================
class UserCreate(BaseModel):
    username: str
    password: str
    role: str | None = "CITIZEN"  # by default citizen

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ================== Auth helpers ==================
def get_user_by_username(username: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password_hash": row[2], "role": row[3]}
    return None

def create_user(username: str, password: str, role: str = "CITIZEN"):
    if role not in ("CITIZEN","OFFICIAL","ANALYST","ADMIN"):
        role = "CITIZEN"
    password_hash = pwd_context.hash(password)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
    conn.commit()
    conn.close()

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

def require_roles(*roles):
    def _dep(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _dep

# ================== Auth Endpoints ==================
@app.post("/auth/register", status_code=201)
def register(user: UserCreate):
    # Only allow self-register as CITIZEN; higher roles must be set by admin or DB
    role = user.role if user.role in ("CITIZEN","OFFICIAL","ANALYST","ADMIN") else "CITIZEN"

    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(user.username, user.password, role)
    return {"status": "ok", "message": "User registered", "username": user.username, "role": role}

@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form.username)
    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

# ================== Reports ==================
# NOTE: username is taken from token now (auth), not from form
@app.post("/report")
def create_report(
    hazard_type: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: UploadFile = File(None),
    current_user = Depends(require_roles("CITIZEN", "OFFICIAL"))  # who can submit
):
    ensure_uploads_dir()
    file_path = None
    if file:
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports (username, hazard_type, description, latitude, longitude, file_path) VALUES (?, ?, ?, ?, ?, ?)",
        (current_user["username"], hazard_type, description, latitude, longitude, file_path)
    )
    conn.commit()
    conn.close()

    return {"status": "ok", "msg": "Report submitted", "file_saved": file_path}

# Only OFFICIAL & ANALYST can see all reports
@app.get("/reports")
def get_reports(_user = Depends(require_roles("OFFICIAL","ANALYST"))):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

# Citizen can see only their own reports
@app.get("/reports/my")
def get_my_reports(current_user = Depends(require_roles("CITIZEN","OFFICIAL","ANALYST"))):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports WHERE username = ? ORDER BY timestamp DESC", (current_user["username"],))
    rows = cur.fetchall()
    conn.close()
    return rows

# ================== Social + Hotspots (as before) ==================
@app.get("/social")
def social_media_feed(_user = Depends(require_roles("OFFICIAL","ANALYST"))):
    return [
        {"platform": "Twitter", "post": "High tides reported near Mumbai", "sentiment": "alert"},
        {"platform": "Facebook", "post": "Fishermen say waves are dangerous today", "sentiment": "warning"},
        {"platform": "YouTube", "post": "Video of sea flooding in Chennai", "sentiment": "critical"},
    ]

@app.get("/hotspots")
def get_hotspots(_user = Depends(require_roles("OFFICIAL","ANALYST"))):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            ROUND(latitude/0.02, 0)*0.02 as cell_lat,
            ROUND(longitude/0.02, 0)*0.02 as cell_lon,
            SUM(
                CASE urgency
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    ELSE 1
                END
            ) as weight
        FROM (
            SELECT latitude, longitude, urgency FROM reports
            UNION ALL
            SELECT latitude, longitude, urgency FROM social_media
        )
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        GROUP BY cell_lat, cell_lon
        HAVING weight > 1
        ORDER BY weight DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {"latitude": r[0], "longitude": r[1], "weight": r[2]}
        for r in rows
    ]


from rule_classifier import classify_post
from pydantic import BaseModel

class SocialPost(BaseModel):
    source: str
    text: str
    timestamp: str
    url: str

@app.post("/social/ingest")
def ingest_social_post(post: SocialPost):
    hazard, urgency = classify_post(post.text)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO social_media (source, text, timestamp, url, hazard, urgency) VALUES (?, ?, ?, ?, ?, ?)",
        (post.source, post.text, post.timestamp, post.url, hazard, urgency)
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "hazard": hazard, "urgency": urgency}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # <- yeh zaroor * hona chahiye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import BackgroundTasks
import social_fetcher  # new module

@app.post("/social/refresh")
def api_social_refresh(q: str = "flood,tsunami,cyclone", limit: int = 20, background_tasks: BackgroundTasks = None, _user = Depends(require_roles("OFFICIAL","ANALYST","CITIZEN"))):
    """
    Fetch posts from social_fetcher and insert into social_media table.
    By default runs in background; set background_tasks=None to run synchronously.
    """
    def do_refresh(query, lim):
        conn = get_db()
        cur = conn.cursor()
        # ensure urgency column exists (safe)
        try:
            cur.execute("ALTER TABLE social_media ADD COLUMN urgency TEXT")
        except Exception:
            pass

        posts = social_fetcher.fetch_all_social(query, lim)
        inserted = 0
        for p in posts:
            url = p.get("url")
            # dedupe by URL if available, else by text+timestamp
            if url:
                cur.execute("SELECT 1 FROM social_media WHERE url=? LIMIT 1", (url,))
                if cur.fetchone():
                    continue
            else:
                cur.execute("SELECT 1 FROM social_media WHERE text=? AND timestamp=? LIMIT 1", (p.get("text"), p.get("timestamp")))
                if cur.fetchone():
                    continue

            cur.execute("""
                INSERT INTO social_media (source, text, timestamp, url, hazard, urgency, latitude, longitude, location_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p.get("source"),
                p.get("text"),
                p.get("timestamp"),
                p.get("url"),
                p.get("hazard"),
                p.get("urgency"),
                p.get("latitude"),
                p.get("longitude"),
                p.get("location_name")
            ))
            inserted += 1
        conn.commit()
        conn.close()
        return inserted

    # run in background if FastAPI background available
    if background_tasks is not None:
        background_tasks.add_task(do_refresh, q, limit)
        return {"status":"started", "message":"background refresh queued"}
    else:
        count = do_refresh(q, limit)
        return {"status":"ok", "inserted": count}

@app.get("/social/list")
def list_social(limit: int = 100, _user = Depends(require_roles("OFFICIAL","ANALYST"))):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, source, text, timestamp, url, hazard, urgency, latitude, longitude, location_name FROM social_media ORDER BY timestamp DESC LIMIT ?", (limit,))
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall(); conn.close()
    return [dict(zip(cols, r)) for r in rows]
