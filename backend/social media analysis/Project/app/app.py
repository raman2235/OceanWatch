import os
import json
import time
from datetime import datetime, timezone
from typing import List, Dict, Any
from collections import defaultdict

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# External SDKs
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

# Load environment variables
load_dotenv()

# ----------------------------
# Configuration
# ----------------------------
DATA_DIR = r"C:\Users\hp\Downloads\Project\data"
os.makedirs(DATA_DIR, exist_ok=True)

# Flask app setup
app = Flask(__name__)
CORS(app)

# ----------------------------
# API Clients
# ----------------------------
# Twitter
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN) if tweepy else None

# Reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
) if praw else None

# YouTube
youtube = gbuild("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")) if gbuild else None

# Instagram
INSTAGRAM_USER_TOKEN = os.getenv("INSTAGRAM_USER_TOKEN")
INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID")

# Google Maps Geocoding API
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


# ----------------------------
# Utility Functions
# ----------------------------
def classify_hazard(text: str) -> str:
    text = text.lower()
    if "flood" in text:
        return "Flood"
    elif "cyclone" in text or "hurricane" in text:
        return "Cyclone"
    elif "tsunami" in text:
        return "Tsunami"
    elif "wave" in text or "high tide" in text:
        return "High Wave"
    else:
        return "Uncategorized"

def geocode_location(location: str):
    """Return (latitude, longitude) for a location using Google Maps API"""
    if not location or not GOOGLE_MAPS_API_KEY:
        return None, None
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data["status"] == "OK" and len(data["results"]) > 0:
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None


# ----------------------------
# Fetch Functions
# ----------------------------
def fetch_twitter_posts(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    posts = []
    if not twitter_client:
        return posts
    try:
        safe_limit = max(10, min(limit, 100))
        tweets = twitter_client.search_recent_tweets(
            query=query, max_results=safe_limit, tweet_fields=["created_at","geo"]
        )

        if tweets.data:
            for tweet in tweets.data:
                lat, lon = None, None
                # Twitter geo is optional
                if tweet.geo:
                    # For simplicity, tweet.geo can contain coordinates
                    pass
                posts.append({
                    "source": "Twitter",
                    "text": tweet.text,
                    "timestamp": tweet.created_at.isoformat(),
                    "url": f"https://twitter.com/i/web/status/{tweet.id}",
                    "hazard": classify_hazard(tweet.text),
                    "latitude": lat,
                    "longitude": lon
                })
    except Exception as e:
        print(f"Twitter error: {e}")
    return posts

def fetch_reddit_posts(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    posts = []
    if not reddit:
        return posts
    try:
        for submission in reddit.subreddit("all").search(query, limit=limit):
            posts.append({
                "source": "Reddit",
                "text": submission.title,
                "timestamp": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).isoformat(),
                "url": submission.url,
                "hazard": classify_hazard(submission.title),
                "latitude": None,
                "longitude": None
            })
    except Exception as e:
        print(f"Reddit error: {e}")
    return posts

def fetch_youtube_posts(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    posts = []
    if not youtube:
        return posts
    try:
        search_response = youtube.search().list(
            q=query, part="snippet", maxResults=min(limit, 50), type="video"
        ).execute()

        for item in search_response.get("items", []):
            snippet = item["snippet"]
            posts.append({
                "source": "YouTube",
                "text": snippet["title"],
                "timestamp": snippet["publishedAt"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "hazard": classify_hazard(snippet["title"]),
                "latitude": None,
                "longitude": None
            })
    except Exception as e:
        print(f"YouTube error: {e}")
    return posts

def fetch_instagram_posts(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    posts = []
    if not INSTAGRAM_USER_TOKEN or not INSTAGRAM_APP_ID:
        return posts
    try:
        url = f"https://graph.facebook.com/v17.0/me/media?fields=caption,media_url,timestamp,permalink&access_token={INSTAGRAM_USER_TOKEN}"
        response = requests.get(url)
        data = response.json()
        if "data" in data:
            for item in data["data"][:limit]:
                caption = item.get("caption", "")
                if query.lower() in caption.lower():
                    posts.append({
                        "source": "Instagram",
                        "text": caption,
                        "timestamp": item.get("timestamp"),
                        "url": item.get("permalink"),
                        "hazard": classify_hazard(caption),
                        "latitude": None,
                        "longitude": None
                    })
    except Exception as e:
        print(f"Instagram error: {e}")
    return posts


# ----------------------------
# Flask Routes
# ----------------------------
@app.route("/")
def home():
    return jsonify({"message": "🌊 Crowdsourced Hazard Reporting API is running!"})


@app.route("/api/refresh", methods=["GET"])
def refresh_data():
    query = request.args.get("q", "flood,tsunami,cyclone")
    limit = int(request.args.get("limit", 10))

    all_posts = []
    for keyword in query.split(","):
        all_posts.extend(fetch_twitter_posts(keyword.strip(), limit))
        all_posts.extend(fetch_reddit_posts(keyword.strip(), limit))
        all_posts.extend(fetch_youtube_posts(keyword.strip(), limit))
        all_posts.extend(fetch_instagram_posts(keyword.strip(), limit))

    # Sort by time
    all_posts.sort(key=lambda x: x["timestamp"], reverse=True)

    # Save to local file
    with open(os.path.join(DATA_DIR, "live_social_media.json"), "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)

    return jsonify({"status": "success", "count": len(all_posts)})


@app.route("/api/social-media", methods=["GET"])
def get_social_media():
    try:
        with open(os.path.join(DATA_DIR, "live_social_media.json"), "r", encoding="utf-8") as f:
            posts = json.load(f)
        return jsonify(posts)
    except FileNotFoundError:
        return jsonify({"error": "No data found. Run /api/refresh first."}), 404


@app.route("/api/report", methods=["POST"])
def submit_report():
    data = request.json
    description = data.get("description")
    location = data.get("location")
    media = data.get("media")

    lat, lon = geocode_location(location)
    report = {
        "id": int(time.time()),
        "description": description,
        "location": location,
        "media": media,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hazard": classify_hazard(description),
        "source": "Citizen",
        "latitude": lat,
        "longitude": lon
    }

    filepath = os.path.join(DATA_DIR, "crowdsourced_reports.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reports = json.load(f)
    except FileNotFoundError:
        reports = []

    reports.append(report)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    return jsonify({"status": "success", "report": report})


@app.route("/api/hotspots", methods=["GET"])
def get_hotspots():
    combined_locations = []

    # Social media posts
    try:
        with open(os.path.join(DATA_DIR, "live_social_media.json"), "r", encoding="utf-8") as f:
            social_posts = json.load(f)
        for post in social_posts:
            if post.get("latitude") and post.get("longitude"):
                combined_locations.append((
                    post.get("location_name", post["text"][:50]),
                    post["latitude"],
                    post["longitude"]
                ))
    except FileNotFoundError:
        pass

    # Citizen reports
    try:
        with open(os.path.join(DATA_DIR, "crowdsourced_reports.json"), "r", encoding="utf-8") as f:
            reports = json.load(f)
        for report in reports:
            if report.get("latitude") and report.get("longitude"):
                combined_locations.append((
                    report.get("location", "Unknown"),
                    report["latitude"],
                    report["longitude"]
                ))
    except FileNotFoundError:
        pass

    # Aggregate hotspots
    hotspot_dict = defaultdict(lambda: {"count": 0, "latitude": 0, "longitude": 0})
    for loc_name, lat, lon in combined_locations:
        key = f"{lat}_{lon}"
        hotspot_dict[key]["count"] += 1
        hotspot_dict[key]["latitude"] = lat
        hotspot_dict[key]["longitude"] = lon
        hotspot_dict[key]["location"] = loc_name

    hotspots = list(hotspot_dict.values())
    hotspots.sort(key=lambda x: x["count"], reverse=True)

    # Save to local file
    hotspots_file = os.path.join(DATA_DIR, "hotspots.json")
    with open(hotspots_file, "w", encoding="utf-8") as f:
        json.dump(hotspots, f, indent=2)

    return jsonify(hotspots)


# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
