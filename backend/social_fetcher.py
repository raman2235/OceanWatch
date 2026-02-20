# social_fetcher.py
import os, json, time
from datetime import datetime, timezone
from typing import List, Dict, Any

# optional SDKs - imported only if installed
try:
    import tweepy
except Exception:
    tweepy = None
try:
    import praw
except Exception:
    praw = None
try:
    from googleapiclient.discovery import build as gbuild
except Exception:
    gbuild = None

import requests
from dotenv import load_dotenv
load_dotenv()

# config
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# instantiate clients if available
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN) if tweepy and TWITTER_BEARER_TOKEN else None
reddit_client = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent="coastal") if praw and REDDIT_CLIENT_ID else None
youtube_client = gbuild("youtube", "v3", developerKey=YOUTUBE_KEY) if gbuild and YOUTUBE_KEY else None

# --- classifiers (simple) ---
def classify_hazard(text: str) -> str:
    t = (text or "").lower()
    if "flood" in t or "flooding" in t:
        return "Flood"
    if "cyclone" in t or "hurricane" in t:
        return "Cyclone"
    if "tsunami" in t:
        return "Tsunami"
    if "wave" in t or "high tide" in t or "swell" in t:
        return "High Wave"
    return "Uncategorized"

def classify_urgency(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["danger", "urgent", "emergency", "critical", "flooding now", "tsunami alert"]):
        return "High"
    if any(k in t for k in ["warning", "alert", "watch", "caution"]):
        return "Medium"
    return "Low"

# --- geocode helper ---
def geocode_location(location: str):
    if not location or not GOOGLE_MAPS_API_KEY:
        return None, None
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(location)}&key={GOOGLE_MAPS_API_KEY}"
        r = requests.get(url, timeout=10)
        j = r.json()
        if j.get("status") == "OK" and j.get("results"):
            loc = j["results"][0]["geometry"]["location"]
            return loc.get("lat"), loc.get("lng")
    except Exception as e:
        print("geocode error:", e)
    return None, None

# --- fetch functions (safe: return empty list if SDK/keys missing) ---
def fetch_twitter_posts(query: str, limit: int = 10) -> List[Dict[str,Any]]:
    out = []
    if not twitter_client:
        # fallback: try to read a local file `data/twitter_mock.json` if present
        fp = os.path.join(DATA_DIR, "twitter_mock.json")
        if os.path.exists(fp):
            try:
                out = json.load(open(fp, "r", encoding="utf-8"))
            except: out = []
        return out
    try:
        tweets = twitter_client.search_recent_tweets(query=query, max_results=min(limit,100), tweet_fields=["created_at","geo"])
        if tweets and getattr(tweets, "data", None):
            for t in tweets.data:
                out.append({
                    "source":"Twitter",
                    "text": t.text,
                    "timestamp": t.created_at.isoformat() if getattr(t, "created_at", None) else datetime.utcnow().isoformat(),
                    "url": f"https://twitter.com/i/web/status/{t.id}",
                    "hazard": classify_hazard(t.text),
                    "latitude": None,
                    "longitude": None,
                    "location_name": None
                })
    except Exception as e:
        print("Twitter fetch error:", e)
    return out

def fetch_reddit_posts(query: str, limit: int = 10) -> List[Dict[str,Any]]:
    out = []
    if not reddit_client:
        fp = os.path.join(DATA_DIR, "reddit_mock.json")
        if os.path.exists(fp):
            try:
                out = json.load(open(fp, "r", encoding="utf-8"))
            except: out = []
        return out
    try:
        for sub in reddit_client.subreddit("all").search(query, limit=limit):
            out.append({
                "source": "Reddit",
                "text": sub.title,
                "timestamp": datetime.fromtimestamp(sub.created_utc, tz=timezone.utc).isoformat(),
                "url": sub.url,
                "hazard": classify_hazard(sub.title),
                "latitude": None, "longitude": None, "location_name": None
            })
    except Exception as e:
        print("Reddit fetch error:", e)
    return out

def fetch_youtube_posts(query: str, limit: int = 10) -> List[Dict[str,Any]]:
    out = []
    if not youtube_client:
        fp = os.path.join(DATA_DIR, "youtube_mock.json")
        if os.path.exists(fp):
            try:
                out = json.load(open(fp, "r", encoding="utf-8"))
            except: out=[]
        return out
    try:
        resp = youtube_client.search().list(q=query, part="snippet", maxResults=min(limit,50), type="video").execute()
        for item in resp.get("items", []):
            snip = item["snippet"]
            out.append({
                "source":"YouTube",
                "text": snip.get("title"),
                "timestamp": snip.get("publishedAt"),
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "hazard": classify_hazard(snip.get("title","")),
                "latitude": None, "longitude": None, "location_name": None
            })
    except Exception as e:
        print("YouTube fetch error:", e)
    return out

def fetch_instagram_posts(query: str, limit: int = 10) -> List[Dict[str,Any]]:
    # Instagram Graph API access is more involved; fallback to local mock if not configured
    fp = os.path.join(DATA_DIR, "instagram_mock.json")
    if os.path.exists(fp):
        try:
            return json.load(open(fp, "r", encoding="utf-8"))
        except:
            return []
    return []


# --- unified fetcher ---
def fetch_all_social(query: str = "flood,tsunami,cyclone", limit: int = 10) -> List[Dict[str,Any]]:
    all_posts = []
    for kw in [k.strip() for k in query.split(",") if k.strip()]:
        all_posts += fetch_twitter_posts(kw, limit)
        all_posts += fetch_reddit_posts(kw, limit)
        all_posts += fetch_youtube_posts(kw, limit)
        all_posts += fetch_instagram_posts(kw, limit)
    # normalize: ensure timestamp and fields present
    for p in all_posts:
        if "timestamp" not in p or not p["timestamp"]:
            p["timestamp"] = datetime.utcnow().isoformat()
        p.setdefault("hazard", classify_hazard(p.get("text","")))
        p.setdefault("urgency", classify_urgency(p.get("text","")))
        p.setdefault("location_name", p.get("location_name"))
    # sort newest first
    try:
        all_posts.sort(key=lambda x: x.get("timestamp",""), reverse=True)
    except:
        pass
    return all_posts
