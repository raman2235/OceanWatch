import sqlite3

DATABASE = "coastal.db"

def classify_post(text: str):
    if not text:
        return "Low"
    t = text.lower()

    if any(word in t for word in ["danger", "emergency", "critical", "very dangerous", "urgent"]):
        return "High"
    elif any(word in t for word in ["warning", "alert", "caution"]):
        return "Medium"
    else:
        return "Low"

def update_urgency():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT id, text FROM social_media")
    rows = cur.fetchall()

    for row in rows:
        record_id, text = row
        urgency = classify_post(text)
        cur.execute("UPDATE social_media SET urgency = ? WHERE id = ?", (urgency, record_id))

    conn.commit()
    conn.close()
    print("✅ Urgency updated for all social media posts")

if __name__ == "__main__":
    update_urgency()
