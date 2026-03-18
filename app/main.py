from fastapi import FastAPI
from services import naive, pessimistic, optimistic
from db import get_connection

app = FastAPI()

@app.post("/book/{strategy}/{seat_id}")
def book(strategy: str, seat_id: str):

    if strategy == "naive":
        success = naive.book(seat_id)

    elif strategy == "pessimistic":
        success = pessimistic.book(seat_id)

    elif strategy == "optimistic":
        success = optimistic.book(seat_id)

    else:
        return {"error": "invalid strategy"}

    return {"success": success}

@app.post("/reset/{seat_id}")
def reset(seat_id: str):
    print("RESET CALLED for", seat_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE seats
        SET status='available', version=0
        WHERE seat_id=%s
        """,
        (seat_id,)
    )

    conn.commit()
    conn.close()

    return {"reset": True}