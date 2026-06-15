# SQL Patterns — ดี vs ไม่ดี (PostgreSQL-first)

> เป้าหมาย: schema ถูกต้อง · query เร็ว+อ่านได้ · **ทุก input เป็น parameter** · migration กลับได้

---

## 1. Schema Design

### ❌ ไม่ดี
```sql
-- type หลวม, ไม่มี constraint, เก็บเงินด้วย float, เวลาเป็น string
CREATE TABLE orders (
  id        varchar,          -- ไม่มี PK ชัด, type ไม่ตรง
  user_id   varchar,          -- ไม่มี FK
  amount    float,            -- ปัดเศษเพี้ยน
  status    varchar,          -- ค่าอะไรก็ใส่ได้
  created   varchar           -- เวลาเป็น text
);
```

### ✅ ดี
```sql
CREATE TABLE users (
  id          bigint generated always as identity PRIMARY KEY,
  email       text NOT NULL UNIQUE,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TYPE order_status AS ENUM ('pending', 'paid', 'cancelled');

CREATE TABLE orders (
  id          bigint generated always as identity PRIMARY KEY,
  user_id     bigint NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  amount      numeric(12,2) NOT NULL CHECK (amount >= 0),  -- เงินใช้ numeric
  status      order_status NOT NULL DEFAULT 'pending',
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
```
- PK ทุกตาราง · FK + `ON DELETE` ชัด · `numeric` สำหรับเงิน · `timestamptz` · `enum`/`CHECK` คุมค่า

---

## 2. Query + Index

### ❌ ไม่ดี
```sql
SELECT * FROM orders o, users u            -- implicit join + SELECT *
WHERE o.user_id = u.id AND u.email = 'a@b.com';
-- ไม่มี index บน users.email → Seq Scan
```

### ✅ ดี
```sql
CREATE INDEX idx_orders_user_id ON orders (user_id);        -- รองรับ JOIN
-- users.email เป็น UNIQUE อยู่แล้ว → มี index ให้

SELECT o.id, o.amount, o.status, o.created_at
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE u.email = $1                         -- parameter ไม่ใช่ค่าตรง
ORDER BY o.created_at DESC
LIMIT 50;

-- ตรวจ plan ก่อนสรุปว่าช้า
EXPLAIN (ANALYZE, BUFFERS)
SELECT ... ;
```

### Pagination — keyset แทน OFFSET ลึก
```sql
-- ❌ ช้าเมื่อ offset ใหญ่ (ต้องสแกนข้ามทุก row)
SELECT * FROM orders ORDER BY id LIMIT 50 OFFSET 100000;

-- ✅ keyset: ส่ง id สุดท้ายของหน้าก่อนเป็น parameter
SELECT id, amount, status
FROM orders
WHERE id > $1                              -- last_seen_id
ORDER BY id
LIMIT 50;
```

### กัน N+1
```sql
-- ❌ N+1: query users ทีละคนในลูป (ฝั่ง app)
--    for id in ids: SELECT * FROM users WHERE id = id

-- ✅ ดึงครั้งเดียว
SELECT id, email FROM users WHERE id = ANY($1);   -- $1 = array ของ id
```

---

## 3. Security — Parameterized vs String Concatenation

### ❌ ไม่ดี — เปิดช่อง SQL injection
```python
# string concat / f-string = อันตราย
email = request.args["email"]
cur.execute("SELECT * FROM users WHERE email = '" + email + "'")
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
# input  ' OR '1'='1  → ดึงทั้งตาราง / ลบข้อมูลได้
```

### ✅ ดี — bind parameter เสมอ
```python
# psycopg (PostgreSQL) — ใช้ %s placeholder + ส่ง params แยก
cur.execute("SELECT id, email FROM users WHERE email = %s", (email,))

# SQLAlchemy Core — text() + bindparams
from sqlalchemy import text
conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
```

### identifier (ชื่อตาราง/คอลัมน์) bind เป็น parameter ไม่ได้ → allowlist
```python
# ❌ f"ORDER BY {col}"  ← injection ผ่านชื่อคอลัมน์
ALLOWED = {"created_at", "amount"}
if col not in ALLOWED:
    raise ValueError("invalid sort column")
sql = f"SELECT id FROM orders ORDER BY {col} DESC"   # col ผ่าน allowlist แล้ว
```

### Connection string — เก็บใน env ไม่ hardcode
```bash
# .env (gitignored) — ใช้ placeholder, ค่าจริงไม่ขึ้น git
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>?sslmode=require   # allowlist secret
```
```python
import os
DATABASE_URL = os.environ["DATABASE_URL"]   # อ่านจาก env ตอน runtime
```
- DB user แบบ least privilege (ไม่ใช้ superuser ใน app) · เปิด `sslmode=require` · ไม่ log SQL ที่มีค่า sensitive
- ตรวจซ้ำด้วย `skill-cybersecurity` / `/skill-cybersecurity-api`

---

## 4. Migration — versioned + reversible

### ❌ ไม่ดี
```sql
-- แก้ schema prod ด้วยมือ ไม่มีไฟล์, ไม่มีทาง rollback
ALTER TABLE orders ADD COLUMN note varchar;
```

### ✅ ดี — มี up/down, zero-downtime
```sql
-- migrations/20260615_01_add_orders_note.up.sql
ALTER TABLE orders ADD COLUMN note text;          -- nullable ก่อน (เข้ากับโค้ดเก่า)

-- migrations/20260615_01_add_orders_note.down.sql
ALTER TABLE orders DROP COLUMN note;
```

### index บนตารางใหญ่ — เลี่ยง lock
```sql
-- ✅ ไม่ lock เขียน (รันนอก transaction)
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);
```
- versioned (commit เข้า git) · เครื่องมือ: Alembic / Flyway / node-pg-migrate / Prisma Migrate
- ไม่แก้ migration ที่ apply แล้ว → ออกตัวใหม่
- เพิ่มคอลัมน์ NOT NULL บนตารางใหญ่: เพิ่ม nullable → backfill → ค่อยเติม `SET NOT NULL`
