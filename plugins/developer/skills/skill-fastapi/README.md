# skills-fastapi

## Overview

`skills-fastapi` คือ skill ที่รวบรวมความรู้ FastAPI ทั้งหมดจาก official documentation และ production best practices ไว้ในที่เดียว ออกแบบมาเพื่อช่วยคุณโด่ง (Data Engineer) เขียนและ review โค้ด FastAPI ได้อย่างถูกต้องตาม standard ตั้งแต่ Basics จนถึง Production Deployment ครอบคลุม use case ที่เกี่ยวข้องกับงาน Data Engineering โดยเฉพาะ

## วิธีการคิดและการทำงานของ Skill

Skill นี้ทำงานเป็น FastAPI Expert ที่มีความรู้ครอบคลุมใน 3 ระดับ:

**ระดับที่ 1 — ตอบจากความรู้ใน SKILL.md (Quick Reference)**
เมื่อถามเรื่อง concept ทั่วไป เช่น "async def ใช้เมื่อไหร่" หรือ "จะ filter response ยังไง" — skill ตอบจาก Quick Reference Rules และตาราง Data Engineering Use Cases ได้ทันที

**ระดับที่ 2 — โหลด reference file ที่เกี่ยวข้อง**
เมื่อต้องการรายละเอียด code pattern เช่น "เขียน CRUD ด้วย SQLModel" หรือ "ตั้งค่า CORS" — skill โหลด reference file ที่ตรงกับ topic เช่น `reference/database.md` หรือ `reference/advanced.md`

**ระดับที่ 3 — เชื่อมโยง use case กับ Data Engineering**
ทุกคำตอบจะถูก map กับ context ของ Data Engineer เช่น pipeline trigger, ML model serving, data ingestion API เพื่อให้คุณโด่งเห็นภาพการใช้งานจริง

**Decision tree ของ skill:**
```
คำถาม/request
    ↓
เป็น code review?  → ตรวจสอบ 10 Quick Reference Rules
เป็น concept?      → อธิบายจาก SKILL.md + ยกตัวอย่าง DE use case
เป็น code gen?     → โหลด reference file + สร้าง code ตาม pattern
เป็น debug?        → วิเคราะห์ error + แนะนำ fix ตาม FastAPI standard
```

## ผลลัพธ์ที่ได้จากการใช้งาน

หลังจากใช้ `skills-fastapi` คุณโด่งจะได้:

- **คำตอบภาษาไทย** พร้อม code ที่ถูกต้องตาม FastAPI standard ล่าสุด (Python 3.10+ syntax)
- **Code patterns** ที่ครบถ้วน — validation, response filtering, error handling, security
- **Best practices** ที่ป้องกันปัญหาที่พบบ่อย เช่น การ expose password, การ block event loop, CORS misconfiguration
- **Production-ready patterns** — Docker, Uvicorn workers, settings management, lifespan events
- **Data Engineering templates** — ML model serving, pipeline API, data ingestion endpoint
- **Reference files** 6 ไฟล์ที่ครอบคลุม topic ทั้งหมดสำหรับใช้เป็น reference ระหว่างพัฒนา

## วิธีใช้

```
/skills-fastapi [topic หรือ คำถาม]
```

หรือ Claude จะ invoke อัตโนมัติเมื่อคุณโด่งถามเรื่อง FastAPI

## ตัวอย่าง

```
/skills-fastapi สร้าง CRUD endpoint สำหรับ data pipeline jobs
/skills-fastapi อธิบาย dependency injection
/skills-fastapi วิธี serve ML model ด้วย lifespan
/skills-fastapi โค้ดนี้ผิด best practice ตรงไหน
```
