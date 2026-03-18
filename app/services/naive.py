from db import get_connection
import time

def book(seat_id: str) -> bool:
    """
    Naive implementation.
    No locking → race condition possible.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM seats WHERE seat_id=%s",
        (seat_id,)
    )
    row = cur.fetchone()

    if row and row[0] == "available":

        time.sleep(0.1)  # amplify race condition

        cur.execute(
            "UPDATE seats SET status='booked' WHERE seat_id=%s",
            (seat_id,)
        )

        conn.commit()
        conn.close()
        return True

    conn.close()
    return False