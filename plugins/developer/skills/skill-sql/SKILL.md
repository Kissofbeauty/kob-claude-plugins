---
name: skill-sql
description: SQL & database expert assistant for writing quality, secure SQL and managing databases (PostgreSQL-first, but covers general SQL). Use when writing/reviewing SQL, designing schema/migrations, or tuning queries. ผู้ช่วยเขียน SQL/ออกแบบ-จัดการ database ให้คุณภาพดีและปลอดภัย (เน้น PostgreSQL ตาม stack มาตรฐานของทีม). Trigger on "เขียน sql", "query", "schema/migration", "database design", or "/skill-sql".
allowed-tools: Read, Glob, Grep, Write, Edit
---

# skill-sql — SQL & Database Standard

ความรู้สำหรับเขียน SQL และจัดการ database ให้ **คุณภาพดีและปลอดภัย** — เน้น **PostgreSQL** เป็นหลัก (stack มาตรฐานของทีม) แต่หลักการครอบ SQL ทั่วไป

> หลักการ: **schema ออกแบบให้ถูกตั้งแต่ต้น · query อ่านได้+ใช้ index · ทุก input เป็น parameter (กัน SQL injection) · migration versioned + reversible**

---

## 🧱 Schema Design

- **Normalization** — เริ่มที่ 3NF (ตัด redundancy/กัน update anomaly) แล้ว denormalize เฉพาะจุดที่วัดผลได้ว่าต้องการ performance จริง
- **Data types ให้แคบและตรงความหมาย** — `int`/`bigint` ตามช่วงค่า, `numeric(p,s)` สำหรับเงิน (ห้าม `float`/`money`), `timestamptz` (ไม่ใช่ `timestamp`) สำหรับเวลา, `text` แทน `varchar(n)` เมื่อไม่จำเป็นต้องจำกัด, `uuid`/`enum`/`jsonb` ตามเหมาะ
- **Keys** — ทุกตารางมี primary key (นิยม surrogate `bigint generated always as identity` หรือ `uuid`), ตั้ง **foreign key** + `ON DELETE` policy ให้ชัด (`RESTRICT`/`CASCADE`/`SET NULL`)
- **Constraints** บังคับ integrity ที่ระดับ DB ไม่ใช่แค่ที่ app — `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`
- ตั้งชื่อสม่ำเสมอ — `snake_case`, ตารางเป็นพหูพจน์ (`users`), คอลัมน์เวลา `created_at`/`updated_at`

→ ตัวอย่าง: `references/sql-patterns.md`

## 🔍 Query

- **เลือกเฉพาะคอลัมน์ที่ใช้** — หลีกเลี่ยง `SELECT *` ใน production code
- **JOIN ชัดเจน** — ใช้ `JOIN ... ON` (ไม่ใช่ join ใน `WHERE`), ระวัง fan-out จาก one-to-many
- **Index ให้ตรง predicate** — สร้าง index บนคอลัมน์ที่ใช้ใน `WHERE`/`JOIN`/`ORDER BY`; composite index เรียงตาม selectivity; partial index เมื่อ query เฉพาะบาง subset
- **อ่าน `EXPLAIN (ANALYZE, BUFFERS)`** ก่อนสรุปว่าช้าตรงไหน — มองหา `Seq Scan` บนตารางใหญ่, ค่า rows ที่ประเมินคลาดเคลื่อน
- **กัน N+1** — ดึงข้อมูลด้วย JOIN/`IN (...)` ครั้งเดียว แทนที่จะ query ในลูปต่อ row (ดู skill-fastapi/ORM)
- **Pagination แบบ keyset** (`WHERE id > :last ORDER BY id LIMIT n`) สำหรับชุดใหญ่ — เร็วและเสถียรกว่า `OFFSET` ที่ลึก ๆ

## 🔒 Security — Parameterized Query (สำคัญที่สุด)

> **ทุก user input ต้องผ่าน parameter/placeholder เสมอ — ห้ามต่อ string สร้าง SQL เด็ดขาด** นี่คือเส้นกั้น SQL injection อันดับหนึ่ง

| ❌ ห้าม | ✅ ทำแทน |
|---|---|
| ต่อ string: `"... WHERE email = '" + email + "'"` | parameter: `WHERE email = $1` / `%s` / `:email` |
| f-string/`format()`/template literal ใส่ค่าลงใน SQL | ส่งค่าเป็น args แยกจาก query string |
| รับชื่อตาราง/คอลัมน์จาก user ตรง ๆ | allowlist ฝั่ง app แล้ว map เป็นชื่อจริง (identifier เป็น parameter ไม่ได้) |

- ใช้ driver/ORM ที่ bind parameter ให้ (psycopg `%s`/`execute(sql, params)`, SQLAlchemy text+bindparams, Prisma/ORM query builder)
- ให้สิทธิ์ DB user แบบ **least privilege** (app ไม่ใช้ superuser), เปิด **SSL** ต่อ DB, อย่า log SQL ที่มีค่า sensitive
- connection string เก็บใน env/secret manager — **ไม่ hardcode** (ดูตัวอย่าง placeholder ใน references)
- เชื่อมโยงมาตรฐานความปลอดภัย → ใช้ **`skill-cybersecurity`** (และ `/skill-cybersecurity-api` สำหรับ endpoint ที่ต่อ DB) ตรวจซ้ำก่อนปิดงาน

## 🔄 Migration

- **Versioned** — ทุกการเปลี่ยน schema เป็นไฟล์ `.sql` ที่ commit เข้า git · **ทีมเขียน SQL migration เอง (ไม่ใช้ Alembic/Flyway/Prisma) — ดูมาตรฐานที่ `skill-data-modeling`** · ห้ามแก้ schema prod ด้วยมือ
- **Reversible** — มี `up` และ `down` (rollback ได้) ทุก migration
- **Forward-only & small** — แต่ละ migration ทำเรื่องเดียว, ไม่แก้ migration ที่ apply ไปแล้ว (ออกตัวใหม่แทน)
- **Zero-downtime patterns** — เพิ่มคอลัมน์เป็น nullable/มี default ก่อน, backfill, ค่อยเพิ่ม constraint; แยก deploy โค้ดกับ migration ให้เข้ากันได้ทั้งเวอร์ชันเก่า/ใหม่
- ระวัง lock — `CREATE INDEX CONCURRENTLY` บนตารางใหญ่ใน production

## ✅ Rules (เช็กก่อนปิดงาน)

1. ทุก input ผ่าน **parameterized query** — ไม่มีการต่อ string สร้าง SQL
2. ตารางมี PK + FK + constraint (`NOT NULL`/`UNIQUE`/`CHECK`) ครบตามความหมายข้อมูล
3. data type ถูกต้อง (`numeric` สำหรับเงิน, `timestamptz` สำหรับเวลา)
4. query สำคัญมี index รองรับ + ตรวจด้วย `EXPLAIN ANALYZE`, ไม่มี N+1
5. การเปลี่ยน schema มาเป็น migration ที่ **versioned + reversible**
6. connection string/secret อยู่ใน env — ไม่ hardcode; DB user แบบ least privilege
7. ผ่าน security check (`skill-cybersecurity`) เมื่อแตะ input/endpoint ที่ต่อ DB

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/sql-patterns.md` | ตัวอย่าง schema / query / index / migration + parameterized vs concat (ดี vs ไม่ดี) |
