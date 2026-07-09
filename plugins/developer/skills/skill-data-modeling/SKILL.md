---
name: skill-data-modeling
description: มาตรฐานออกแบบ data model ของทีม — (1) primary key = UUID v7 สร้างที่ backend (2) soft-delete + timestamps ทุกตาราง (3) เกณฑ์ตัดสินสร้างตารางใหม่หรือขยายตารางเดิม (4) ไฟล์/รูปเก็บที่ S3 ส่วน DB เก็บ metadata (5) migration เขียน SQL เอง. ใช้เมื่อออกแบบหรือรีวิว schema / data model. Trigger on "ออกแบบ schema", "data model", "ตารางใหม่", "primary key", "soft delete", "เก็บไฟล์/รูป", "/skill-data-modeling"
allowed-tools: Read, Glob, Grep
---

# skill-data-modeling — Data Modeling Standard

มาตรฐานการออกแบบ **data model** ขององค์กร (PostgreSQL) — ใช้เป็นเกณฑ์เมื่อออกแบบ/รีวิว schema

> หลักการ: **PK = UUID v7 สร้างที่ backend · ตารางหลัก soft-delete · ยึด 3NF + เกณฑ์ 4 คำถาม · ไฟล์ไป S3, DB เก็บ metadata · migration = SQL เขียนเอง**
> HOW ของ SQL/query/index/migration → ดู **`skill-sql`** (skill นี้บอก "ออกแบบอะไร" ไม่ใช่ "เขียน SQL ยังไง")

---

## 1. 🔑 Primary Key = UUID v7 (ทุกตาราง)

- ทุกตารางใช้ **UUID v7** เป็น primary key — time-ordered จึง index ได้ดีกว่า UUID v4 และใช้ร่วมข้ามระบบได้
- **สร้างที่ backend เสมอ** : เพราะ PostgreSQL ของทีม (17.x) ยังไม่มีฟังก์ชัน `uuidv7()` ในตัว รวมถึงไม่มีแผนอัปเกรด DB และ DB ของทีม (17.x) สร้างเองไม่ได้
- library มาตรฐานต่อภาษา (ตายตัว — ทั้งคู่ตาม **RFC 9562** จึงได้ id ที่เข้ากันข้ามระบบ):

| Backend | Library | เงื่อนไข |
|---|---|---|
| Python (FastAPI) | **`uuid-utils`** | Python ≥ 3.11 · ใช้ตัวนี้ตัวเดียวทุกเวอร์ชัน Python |
| TypeScript (Next.js API) | **`uuid`** (uuidjs) | เวอร์ชัน ≥ 11 |

- DB เก็บ PK เป็น **native `uuid` type เท่านั้น** — ❌ ห้ามเก็บเป็น `text`/`varchar` (เปลืองพื้นที่ + index ช้า + เสีย type safety)
- FK ที่อ้างถึงก็เป็น `uuid` ตามกัน

## 2. 🗑️ Soft-delete + Timestamps

**Timestamps — ทุกตาราง ไม่มีข้อยกเว้น:**
- `created_at`, `updated_at` (ชนิด `timestamptz` — ดู data types ใน `skill-sql`)

**Soft-delete (`deleted_at`) — เฉพาะตารางหลัก:** ใช้ "เกณฑ์ตัดสิน" ไม่ใช่รายชื่อตาราง (ผู้ออกแบบชี้ตารางจริงตอนทำโปรเจกต์):

| ใส่ `deleted_at` (soft delete) | ไม่ใส่ (hard delete ได้เลย) |
|---|---|
| ตาราง **ตัวตน** (เช่น ผู้ใช้ ลูกค้า สินค้า) | ตาราง **เชื่อม** (junction/many-to-many) |
| ตาราง **ธุรกรรมหลัก** (เช่น คำสั่งซื้อ การชำระเงิน) | ตาราง **lookup / enum / config** |
| ข้อมูลที่ลบแล้วต้องกู้คืน/ตรวจสอบย้อนหลังได้ | ตาราง **cache / session / log ชั่วคราว** |

- query ปกติของตารางที่มี `deleted_at` ต้องกรอง `WHERE deleted_at IS NULL` เสมอ (พิจารณา partial index — ดู `skill-sql`)
- 🟡 **รอ legal:** ระยะเวลาเก็บก่อนลบจริง (retention) + ขอบเขต PDPA — ตัวเลขประมาณการ ~3 ปี แต่**ยังไม่เคาะ ห้ามเขียนตายตัวในโปรเจกต์** จนกว่าฝ่ายกฎหมาย/Lead BI ยืนยัน

## 3. 📐 สร้างตารางใหม่ vs ขยายตารางเดิม (เกณฑ์ 4 คำถาม)

หลักพื้นฐาน = **3NF** (ดู `skill-sql` Schema Design) เมื่อมีข้อมูลใหม่เข้ามา ถามทีละข้อ:

| # | คำถาม | ตัวอย่าง |
|---|---|---|
| 1 | ข้อมูลนี้เป็น **one-to-many** กับของเดิมไหม? | สินค้า 1 ชิ้นมีหลายรูป |
| 2 | มัน **มีคุณสมบัติของตัวเอง** หลายอย่างไหม? | ที่อยู่มีถนน/เขต/รหัสไปรษณีย์ |
| 3 | มันจะ **ถูกตารางอื่นอ้างถึง (FK)** ไหม? | หมวดหมู่ถูกอ้างจากหลายที่ |
| 4 | มันเป็น **คนละแนวคิด (concept)** กับตารางเดิมไหม? | "การจัดส่ง" ไม่ใช่ "คำสั่งซื้อ" |

> ตอบ **"ใช่" แม้ข้อเดียว → สร้างตารางใหม่** · ตอบ "ไม่" ทุกข้อ → ขยายคอลัมน์ในตารางเดิมได้

## 4. 🖼️ ไฟล์ / รูปภาพ → S3 (DB เก็บแค่ metadata)

- ไฟล์และรูปทุกชนิด **ห้ามเก็บลง DB** (ไม่ใช้ `bytea`/base64) → เก็บใน **object storage: S3** (ฝั่ง AWS เดียวกับ prod)
- DB เก็บเฉพาะ **metadata** เช่น `bucket`, `object_key`, `mime_type`, `size_bytes`, `uploaded_at` (+ FK ไปเจ้าของไฟล์)
- การตั้งค่า bucket ให้ปลอดภัย (block public access, encryption) → ดู `skill-cybersecurity-container-iac`

## 5. 🔄 Migration = SQL เขียนเอง (ไม่ใช้เครื่องมือ migration)

- **มติทีม:** เขียนไฟล์ `.sql` เอง — เพราะ backend มี 2 ภาษา (Next.js/TypeScript และ FastAPI/Python) เครื่องมืออย่าง Alembic/Drizzle ผูกกับภาษาเดียว มาตรฐานเดียวที่ครอบทั้งคู่คือ SQL ล้วน
- ⚠️ **ข้อนี้ override คำแนะนำเครื่องมือใน skill อื่น** — จุดที่ `skill-sql` / `skill-fastapi` กล่าวถึง Alembic / Flyway / node-pg-migrate / Prisma Migrate ให้ยึดมตินี้แทน (หลักการ versioned + reversible ของ `skill-sql` ยังใช้เต็ม เปลี่ยนเฉพาะเครื่องมือ)
- convention ที่ต้องมี (เพราะ SQL เปล่าไม่มี versioning ในตัว):
  1. **ชื่อไฟล์มีลำดับ**: `NNNN_คำอธิบาย.sql` เช่น `0001_create_users.sql`, `0002_add_orders.sql`
  2. **ตาราง migration history** ใน DB — บันทึกว่า apply ไฟล์ไหนไปแล้วเมื่อไร
  3. **ทุก migration มี up / down** (rollback ได้) — ตามมาตรฐาน `skill-sql`
- HOW ทั้งหมด (reversible, forward-only, zero-downtime, `CREATE INDEX CONCURRENTLY`) → **`skill-sql` Migration** ไม่เขียนซ้ำที่นี่

---

## ✅ Rules (เช็กก่อนปิดงานออกแบบ)

1. ทุกตาราง: PK = **UUID v7** สร้างที่ backend ด้วย library มาตรฐานต่อภาษา · เก็บเป็น native `uuid`
2. ทุกตาราง: มี `created_at`, `updated_at` (`timestamptz`)
3. ตารางหลัก (ตามเกณฑ์ข้อ 2): มี `deleted_at` + ทุก query กรอง `deleted_at IS NULL`
4. ตัดสิน "ตารางใหม่ vs ขยายเดิม" ด้วย 4 คำถาม + ยึด 3NF
5. ไฟล์/รูปอยู่ที่ S3 ส่วน DB มีแค่ metadata
6. การเปลี่ยน schema ทุกครั้ง = ไฟล์ `.sql` มีเลขลำดับ + up/down + ลง history table (HOW → `skill-sql`)
7. ไม่ฟันตัวเลข retention/PDPA จนกว่า legal ยืนยัน (🟡 มาร์ค "รอ" ในเอกสารโปรเจกต์)

## 🟡 จุดที่ยังรอเคาะ (อย่าตัดสินใจแทน)

| เรื่อง | สถานะ |
|---|---|
| retention policy (ลบจริงหลังกี่วัน/ปี) + ขอบเขต PDPA | รอฝ่ายกฎหมาย + Lead BI ยืนยัน |
| สายการถามเมื่อ business rule ไม่ชัด (ผ่าน skill-PM ก่อนถึงคน) | ทีม BI ปรับ — รอแจ้ง Lead BI รับทราบ |

## เชื่อมโยง skill อื่น

- เขียน SQL / query / index / migration HOW → **`skill-sql`**
- โครงชั้น backend ที่เรียกใช้ data layer → **`skill-backend`** · Python → **`skill-fastapi`**
- ความปลอดภัย S3 / IaC → **`skill-cybersecurity-container-iac`**