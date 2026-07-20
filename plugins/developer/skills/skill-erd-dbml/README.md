# skill-erd-dbml

## Overview
Skill สำหรับสร้าง/อัปเดต **ภาพ ERD** ของโปรเจกต์เป็น 2 ไฟล์: `docs/erd.dbml` (โครงสร้างตาราง + เส้นความสัมพันธ์ เปิดดูแผนภาพได้ใน dbdiagram.io) และ `docs/erd-readme.md` (คู่มืออ่านแผนภาพสำหรับคนไม่รู้ technical) เป็น deliverable บังคับของ `subagent-data-architect` คู่กับ `docs/data-model.md`

## วิธีการคิดและการทำงานของ Skill
- **กฎ 3 ไฟล์คู่กัน:** data model เปลี่ยนเมื่อไร → `data-model.md` + `erd.dbml` + `erd-readme.md` ต้องอัปเดตพร้อมกันเสมอ
- **เลือกโหมดตามสถานะโปรเจกต์:**
  - โหมด A (ช่วงออกแบบ ยังไม่มี `.sql`) → เขียน DBML ตรงจาก design ใน `data-model.md`
  - โหมด B (มีไฟล์ migration แล้ว) → gen จาก `.sql` ด้วย `sql2dbml` + helper script `scripts/sql-fk-to-dbml.mjs` (เติม FK แบบ `ALTER TABLE` ที่ sql2dbml ทิ้ง + จัดโซนสีต่อ Postgres schema) เพื่อกัน drift — ห้ามแก้ไฟล์ derived ด้วยมือ
- cardinality ตาม DBML spec: `>` many-to-one · `-` 1:1 · `<>` m:n

## ผลลัพธ์ที่ได้จากการใช้งาน
- `docs/erd.dbml` — วางใน https://dbdiagram.io/d แล้วเห็นแผนภาพตารางพร้อมเส้นความสัมพันธ์ (+โซนสีถ้ามีหลาย schema)
- `docs/erd-readme.md` — user ที่ไม่รู้ technical เปิดดูโครงสร้างข้อมูลเองได้ตามขั้นตอนในไฟล์ · ทีม technical เห็นภาพรวม schema โดยไม่ต้องไล่อ่าน SQL

## วิธีใช้
```
/skill-erd-dbml
```
หรือให้ subagent-data-architect เรียกอัตโนมัติเมื่อออกแบบ/แก้ data model

## ตัวอย่าง
```
/skill-erd-dbml   # หลังแก้ docs/data-model.md หรือมี migration ใหม่ → refresh erd.dbml + erd-readme.md
```
