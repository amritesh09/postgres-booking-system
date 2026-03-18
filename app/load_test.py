import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE = "http://localhost:8000/book"

def reset():
    requests.post("http://localhost:8000/reset/A1")

def run_test(strategy):
    reset()
    url = f"{BASE}/{strategy}/A1"

    success = 0
    fail = 0

    def hit(_):
        nonlocal success, fail
        r = requests.post(url)
        data = r.json()
        if data["success"]:
            success += 1
        else:
            fail += 1

    start = time.time()

    with ThreadPoolExecutor(max_workers=100) as executor:
        list(executor.map(hit, range(100)))

    duration = round(time.time() - start, 2)
    return {
        "strategy": strategy,
        "success": success,
        "fail": fail,
        "time": duration
    }

if __name__ == "__main__":
    results = [
        run_test("naive"),
        run_test("pessimistic"),
        run_test("optimistic")
    ]

    print("\nRESULTS")
    for r in results:
        print(r)