from fastapi import FastAPI

app = FastAPI()

@app.post("/reset/{seat_id}")
def reset(seat_id: str):
    """
    Reset seat to initial state.
    Used before each load test run.
    """

    from db import get_connection

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE seats
        SET status = 'available',
            version = 0
        WHERE seat_id = %s
        """,
        (seat_id,)
    )

    conn.commit()
    conn.close()

    return {"reset": True}