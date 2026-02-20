import sqlite3

conn = sqlite3.connect("coastal.db")
cur = conn.cursor()

# --- reports table (already in your file) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    hazard_type TEXT,
    description TEXT,
    latitude REAL,
    longitude REAL,
    file_path TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# --- NEW: users table + unique username + role ---
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('CITIZEN','OFFICIAL','ANALYST','ADMIN')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS social_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    text TEXT,
    timestamp TEXT,
    url TEXT,
    hazard TEXT,
    urgency TEXT,   -- added by classifier
    latitude REAL,
    longitude REAL,
    location_name TEXT
)
""")

conn.commit()
conn.close()
