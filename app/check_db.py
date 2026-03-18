import psycopg2

conn = psycopg2.connect(
    dbname="booking",
    user="postgres",
    password="postgres",
    host="db",
    port=5432
)

cur = conn.cursor()
cur.execute("SELECT * FROM seats")

print(cur.fetchall())

conn.close()