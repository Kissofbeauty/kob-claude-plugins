# skill-python

## Overview
ผู้เชี่ยวชาญ Python สำหรับเขียน/review/อธิบายโค้ดให้ถูกตาม PEP8, OOP, SOLID, design patterns, advanced features และ clean architecture — ปรับให้เข้าธีมโปรเจกต์ kob (บังคับใช้ **venv แยกต่อ project**, ไม่มี secret ในโค้ด, เชื่อมกับ skill-fastapi/backend/sql/git-standard)

## วิธีการคิดและการทำงานของ Skill
1. **ธีมโปรเจกต์ก่อน** — venv แยก (ไม่ใช้ base), อ่าน secret จาก env, ผูกกับ skill อื่นในทีม
2. **มาตรฐานโค้ด** — PEP8, type hints ทุก signature, dataclass/Protocol/ABC ตามเหมาะ
3. **สถาปัตยกรรม** — layers + dependency rule + repository + DI; business logic แยกชั้น
4. **อ้าง reference** — รายละเอียด PEP8/OOP/SOLID/advanced/structure อยู่ใน `reference/`

## ผลลัพธ์ที่ได้จากการใช้งาน
- โค้ด Python คุณภาพดี ตาม standard + type-safe + แยกชั้นชัด
- โปรเจกต์ Python ตั้ง env ถูก (venv ต่อ project) ไม่เลอะ base
- ส่งต่อ qa-tester/security ผ่านง่ายขึ้น

## วิธีใช้
```
/skill-python
/skill-python "decorator กับ context manager ต่างกันยังไง"
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อเขียน/review Python

## ตัวอย่าง
```
user: "เริ่ม service Python ใหม่"
→ skill แนะนำ: สร้าง .venv แยก, โครง src/+tests/+pyproject.toml,
  type hints + repository pattern, ไม่ hardcode secret
```
