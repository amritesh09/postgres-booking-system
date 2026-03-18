import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="booking",
        user="postgres",
        password="postgres",
        host="db",
        port=5432
    )