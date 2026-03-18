from db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS seats (
    seat_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    version INT NOT NULL DEFAULT 0
)
""")

cur.execute("""
INSERT INTO seats (seat_id, status)
VALUES ('A1','available')
ON CONFLICT (seat_id) DO NOTHING
""")

conn.commit()
conn.close()

print("Database initialized")