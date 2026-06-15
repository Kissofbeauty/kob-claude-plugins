# skill-sql

## Overview
ความรู้สำหรับ subagent-fullstack (และ dev) ในการ **เขียน SQL และจัดการ database ให้คุณภาพดีและปลอดภัย** เน้น **PostgreSQL** ตาม stack มาตรฐานของทีม แต่หลักการครอบ SQL ทั่วไป ครอบคลุม schema design, query/index tuning, **security (parameterized query กัน SQL injection)** และ migration ที่ versioned + reversible

## วิธีการคิดและการทำงานของ Skill
1. **Schema ถูกตั้งแต่ต้น** — normalization (3NF), data type ตรงความหมาย (`numeric` เงิน, `timestamptz` เวลา), PK/FK/constraint ครบ
2. **Query เร็ว+อ่านได้** — JOIN ชัด, index ตรง predicate, อ่าน `EXPLAIN ANALYZE`, กัน N+1, pagination แบบ keyset
3. **Security มาก่อน** — ทุก input ผ่าน **parameterized query** เสมอ (ห้ามต่อ string), least privilege, secret ใน env — ผูกกับ `skill-cybersecurity`
4. **Migration ปลอดภัย** — versioned + reversible (up/down), zero-downtime, ไม่แก้ schema prod ด้วยมือ

## ผลลัพธ์ที่ได้จากการใช้งาน
- SQL/schema/migration ที่ได้มาตรฐาน ปลอดภัยจาก SQL injection
- query ที่มี index รองรับและตรวจสอบ performance ด้วย `EXPLAIN`
- โครง migration ที่ rollback ได้และ commit เข้า git

## วิธีใช้
```
/skill-sql
/skill-sql            # เมื่อจะเขียน query / ออกแบบ schema / ทำ migration
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อทำงานกับ SQL/database design/query/migration

## ตัวอย่าง
```
user: "เขียน query ดึง order ล่าสุดของ user ตาม email"
→ skill เขียน SELECT แบบ parameterized ($1), JOIN ชัดเจน, แนะนำ index บน
  user_id/email, ใช้ keyset pagination, และเตือนให้ตรวจ EXPLAIN ANALYZE
```
