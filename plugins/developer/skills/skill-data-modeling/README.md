# skill-data-modeling

## Overview
มาตรฐานการออกแบบ data model ขององค์กร (PostgreSQL)  — ครอบเรื่อง primary key (UUID v7), soft-delete + timestamps, เกณฑ์ตัดสินใจสร้างตารางใหม่หรือขยายตารางเดิม, การเก็บไฟล์/รูปบน S3 และ convention ของ migration แบบเขียน SQL เอง ใช้เป็นคู่มือหลักของ `subagent-data-architect` และผู้ที่ออกแบบ/รีวิว schema

## วิธีการคิดและการทำงานของ Skill
- ให้ "เกณฑ์ตัดสิน" ไม่ใช่รายการตายตัว — เช่น soft-delete ระบุเป็นเกณฑ์ประเภทตาราง ให้ผู้ออกแบบชี้ตารางจริงตอนทำโปรเจกต์
- ตัดสิน "สร้างตารางใหม่ vs ขยายเดิม" ด้วยคำถาม 4 ข้อ — ใช่ข้อเดียวคือสร้างใหม่ บนหลัก 3NF
- แบ่งเขตกับ skill ข้างเคียงชัดเจน: skill นี้บอก "ออกแบบอะไร" ส่วน HOW ของ SQL/query/migration อ้างไป `skill-sql` ไม่เขียนซ้ำ
- จุดที่มติทีม override คำแนะนำเดิม (เครื่องมือ migration → SQL เขียนเอง) ระบุไว้ชัดเพื่อกันความสับสนเมื่ออ่านหลาย skill พร้อมกัน


## ผลลัพธ์ที่ได้จากการใช้งาน
- schema ที่ทุกตารางใช้ UUID v7 (backend-generated, native `uuid`), มี timestamps ครบ, soft-delete ถูกที่
- โครงสร้างตารางที่ผ่านเกณฑ์ 3NF + 4 คำถาม พร้อมเหตุผลอ้างอิงได้
- แนวการเก็บไฟล์ที่ถูกมาตรฐาน (S3 + metadata ใน DB)
- แผน migration ที่เป็นไฟล์ `.sql` มีเลขลำดับ + up/down + history table ตามมาตรฐานทีม
- เอกสาร data model ทั้งหมดเก็บไว้ที่ `docs/data-model.md` (ที่เดียว เป็น source of truth ของ schema)

## วิธีใช้
```
/skill-data-modeling
```
หรือถูกเรียกอัตโนมัติเมื่อพูดถึงการออกแบบ schema / data model / ตาราง / ตารางใหม่ / soft delete

## ตัวอย่าง
```
/skill-data-modeling ออกแบบตารางสำหรับระบบสั่งซื้อที่มีสินค้า รูปสินค้า และการชำระเงิน
```