# PostgreSQL High-Contention Booking System

## Overview

This project explores concurrency control and transactional correctness in PostgreSQL under high contention.

It simulates multiple users attempting to book the same seat simultaneously and compares three strategies:

- Naive (no locking)
- Pessimistic locking (`SELECT FOR UPDATE`)
- Optimistic locking (version-based)

The goal is to understand how relational databases handle race conditions and how different approaches impact correctness, throughput, and latency.

---

## Problem Statement

Multiple concurrent users attempt to book the same seat.

How do we prevent:

- Double booking
- Lost updates
- Inconsistent state

---

## Architecture

Client  
↓  
FastAPI Service  
↓  
PostgreSQL  

PostgreSQL acts as the single source of truth and enforces transactional guarantees.

---

## Data Model

```

seats (
seat_id TEXT PRIMARY KEY,
status TEXT NOT NULL,
version INT NOT NULL DEFAULT 0
)

```

- `status`: available / booked  
- `version`: used for optimistic locking  

---

## Implemented Strategies

### 1️⃣ Naive (No Locking)

**Approach**
- Read seat status
- If available → update

**Issue**
- Multiple transactions read "available" before update
- Leads to double booking

**Result**
- ❌ Incorrect under concurrency
- ❌ Race condition (lost update problem)

---

### 2️⃣ Pessimistic Locking

**Approach**
```

SELECT ... FOR UPDATE

```

- Locks the row inside a transaction
- Other transactions must wait

**Properties**
- Guarantees correctness
- Serializes access

**Tradeoff**
- Lower throughput under contention
- Higher latency due to blocking

**Result**
- ✅ Exactly one booking succeeds
- ❌ Reduced concurrency

---

### 3️⃣ Optimistic Locking

**Approach**
```

UPDATE ... WHERE version = X

```

- No locks
- Uses version column to detect conflicts

**Properties**
- Non-blocking
- Conflict detection instead of prevention

**Tradeoff**
- Requires retry logic for robustness

**Result**
- ✅ Prevents double booking
- ⚠️ May fail under high contention without retries

---

## Load Testing

Simulates concurrent requests using a thread pool.

Configuration:

- 100 requests
- 100 concurrent workers
- Same seat (`A1`) → hotspot scenario

---

## Example Results

```

{'strategy': 'naive', 'success': 15, 'fail': 85, 'time': 1.16}
{'strategy': 'pessimistic', 'success': 1, 'fail': 99, 'time': 1.02}
{'strategy': 'optimistic', 'success': 1, 'fail': 99, 'time': 0.95}

```

---

## Key Learnings

### 1️⃣ Race Conditions Are Real

Naive implementation allowed multiple successful bookings.

Multiple transactions read stale state and commit independently.

---

### 2️⃣ Pessimistic Locking Ensures Correctness

- Guarantees only one success
- Serializes access
- Trades performance for safety

---

### 3️⃣ Optimistic Locking Scales Better

- Avoids blocking
- Works well when contention is low
- Requires retries for correctness

---

### 4️⃣ Concurrency Bugs Are Timing-Dependent

Artificial delay was introduced to:

- Increase overlap between requests
- Make race conditions reproducible

---

### 5️⃣ Correctness vs Throughput Tradeoff

| Strategy      | Correctness | Throughput | Latency |
|--------------|------------|------------|---------|
| Naive        | ❌         | ✅         | Low     |
| Pessimistic  | ✅         | ❌         | Higher  |
| Optimistic   | ✅         | ✅         | Medium  |

---

## API Endpoints

```

POST /book/{strategy}/{seat_id}
POST /reset/{seat_id}

```

Strategies:

- `naive`
- `pessimistic`
- `optimistic`

---

## How To Run

### 1️⃣ Install dependencies

```

pip install -r requirements.txt

```

---

### 2️⃣ Initialize database

```

python init_db.py

```

---

### 3️⃣ Start server

```

uvicorn main:app --host 0.0.0.0 --port 8000

```

---

### 4️⃣ Run load test

```

python load_test.py

```

---

## Why This Project Exists

This project was built to understand:

- Transaction isolation
- Row-level locking
- Lost update problem
- Optimistic vs pessimistic concurrency
- Real-world contention behavior

It complements distributed system learning (e.g., rate limiter) with strong consistency guarantees in relational systems.

---

## Future Improvements

- Add retry logic for optimistic locking
- Measure latency distribution
- Add connection pooling
- Simulate multi-seat booking
- Explore isolation levels (READ COMMITTED, SERIALIZABLE)
