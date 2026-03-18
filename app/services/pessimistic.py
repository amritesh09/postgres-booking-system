from db import get_connection
import time

def book(seat_id: str) -> bool:
    """
    Pessimistic locking using SELECT FOR UPDATE.
    Ensures only one transaction can modify row.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("BEGIN")

    cur.execute(
        "SELECT status FROM seats WHERE seat_id=%s FOR UPDATE",
        (seat_id,)
    )

    row = cur.fetchone()

    if row and row[0] == "available":

        time.sleep(0.1)  # simulate contention

        cur.execute(
            "UPDATE seats SET status='booked' WHERE seat_id=%s",
            (seat_id,)
        )

        conn.commit()
        conn.close()
        return True

    conn.rollback()
    conn.close()
    return False