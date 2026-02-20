import sqlite3
conn = sqlite3.connect("coastal.db")
cur = conn.cursor()
cur.execute("SELECT id, source, hazard, urgency, text FROM social_media LIMIT 10")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
