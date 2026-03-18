from db import get_connection
import time

def book(seat_id: str) -> bool:
    """
    Optimistic locking using version column.
    No locks → conflict detected via version mismatch.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status, version FROM seats WHERE seat_id=%s",
        (seat_id,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    status, version = row

    if status != "available":
        conn.close()
        return False

    time.sleep(0.1)  # simulate contention

    cur.execute(
        """
        UPDATE seats
        SET status='booked', version=version+1
        WHERE seat_id=%s AND version=%s
        """,
        (seat_id, version)
    )

    if cur.rowcount == 1:
        conn.commit()
        conn.close()
        return True

    conn.rollback()
    conn.close()
    return False