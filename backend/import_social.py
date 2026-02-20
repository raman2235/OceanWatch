import sqlite3, json, glob

DATABASE = "coastal.db"

def insert_post(post):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO social_media (source, text, timestamp, url, hazard, urgency, latitude, longitude, location_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        post.get("source"),
        post.get("text"),
        post.get("timestamp"),
        post.get("url"),
        post.get("hazard"),
        post.get("urgency"),  # may be None for now
        post.get("latitude"),
        post.get("longitude"),
        post.get("location_name")
    ))
    conn.commit()
    conn.close()

def import_from_folder(folder="data/"):
    for file in glob.glob(f"{folder}/*.json"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]  # single object
                for post in data:
                    insert_post(post)
                print(f"✅ Imported {len(data)} records from {file}")
            except Exception as e:
                print(f"❌ Error in {file}: {e}")

if __name__ == "__main__":
    import_from_folder("C:\coastal-backend\social media analysis\Project\data")  # change to your folder path
