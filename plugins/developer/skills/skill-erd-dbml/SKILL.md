---
name: skill-erd-dbml
description: สร้าง/อัปเดต docs/erd.dbml + docs/erd-readme.md ให้ตรง data model ล่าสุด มีเส้น relationships ครบ เปิดดูแผนภาพได้ใน dbdiagram.io. ใช้ทุกครั้งที่ data model เปลี่ยน (คู่กับ docs/data-model.md). Trigger: "อัปเดต erd", "er diagram", "gen dbml", "dbdiagram", "schema diagram", "/skill-erd-dbml"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# skill-erd-dbml — ภาพ ERD เป็น DBML (พร้อม Relationships)

ทำ **ภาพโครงสร้างข้อมูล (ERD)** ของโปรเจกต์เป็น 2 ไฟล์ใน `docs/` — ให้ทีม technical ทำงานต่อได้สะดวก และ user ที่ไม่รู้ technical ก็เปิดดูได้:

| ไฟล์ | คืออะไร |
|---|---|
| `docs/erd.dbml` | ตาราง + เส้นความสัมพันธ์ ในภาษา DBML — วางใน dbdiagram.io แล้วเห็นแผนภาพทันที |
| `docs/erd-readme.md` | คู่มือประกอบ: วิธีเปิดดูแผนภาพ (ภาษาคน ไม่ต้องรู้ technical) + สรุปว่าแต่ละตารางเก็บอะไร |

## 🔗 กฎ 3 ไฟล์คู่กัน (สำคัญที่สุด)

**ทุกครั้งที่ data model เปลี่ยน** ต้องอัปเดต 3 ไฟล์นี้พร้อมกันเสมอ — ห้ามอัปเดตแค่บางไฟล์:

```
docs/data-model.md  (design — source of truth)
docs/erd.dbml       (แผนภาพ — ต้องตรง design)
docs/erd-readme.md  (คู่มืออ่านแผนภาพ)
```

## โหมดการทำงาน (เลือกตามสถานะโปรเจกต์)

### โหมด A — ช่วงออกแบบ (ยังไม่มีไฟล์ migration `.sql`)
subagent-data-architect ออกแบบเสร็จใน `docs/data-model.md` แล้ว **เขียน `docs/erd.dbml` ตรงจาก design**:

```dbml
Table users {
  id uuid [pk, note: 'UUID v7 gen ที่ backend']
  email text [not null, unique]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table orders {
  id uuid [pk]
  user_id uuid [not null]
  amount "numeric(12,2)" [not null]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
  deleted_at timestamptz [note: 'soft delete — ตารางธุรกรรมหลัก']
}

Ref: orders.user_id > users.id   // > = many-to-one
```

### โหมด B — โปรเจกต์มีไฟล์ migration แล้ว (gen จาก `.sql` กัน drift)
รันที่ root ของ repo (path migration ตามโปรเจกต์ เช่น `migrations/` หรือ `db/migrations/`):

```bash
# รวม migration ทุกไฟล์ตามลำดับเลข (⚠️ เอาเฉพาะส่วน up — อย่ารวม down/rollback)
cat migrations/[0-9]*.sql > /tmp/schema-all.sql

# 1) tables + columns + enums (เขียนทับ docs/erd.dbml)
npx --package=@dbml/cli sql2dbml /tmp/schema-all.sql --postgres -o docs/erd.dbml

# 2) เติม relationships (FK แบบ ALTER TABLE ที่ sql2dbml ทิ้ง) + โซนต่อ schema ต่อท้ายไฟล์
node <skill-dir>/scripts/sql-fk-to-dbml.mjs /tmp/schema-all.sql >> docs/erd.dbml
```

> `<skill-dir>` = โฟลเดอร์ของ skill นี้ (เช่น `plugins/developer/skills/skill-erd-dbml`)
> โหมด B แล้ว **อย่าแก้ `erd.dbml` ด้วยมือ** (เป็นไฟล์ derived) — ยกเว้นปรับ `>` → `-` กรณี FK ติด UNIQUE (= 1:1)

### helper script ทำอะไร (`scripts/sql-fk-to-dbml.mjs`)
- จับทุก `ALTER TABLE … FOREIGN KEY (cols) REFERENCES …` → emit `Ref:` (sql2dbml ข้าม pattern นี้ ทำให้ตารางลอยไม่มีเส้น · FK ที่เขียน inline ใน `CREATE TABLE` sql2dbml จัดการเองแล้ว)
- รองรับชื่อ quoted/unquoted · มี/ไม่มี schema (ไม่มี = `public`) · single + composite FK · รับหลายไฟล์
- ถ้ามีหลาย Postgres schema → จัด `TableGroup` เป็นโซนสีต่อ schema ให้อัตโนมัติ

## DBML standard (spec: https://dbml.dbdiagram.io/docs/)

| op | ความหมาย | ตัวอย่าง |
|---|---|---|
| `<` | one-to-many | `users.id < posts.user_id` |
| `>` | **many-to-one** (FK ปกติ) | `posts.user_id > users.id` |
| `-` | one-to-one | `users.id - user_infos.user_id` |
| `<>` | many-to-many | `authors.id <> books.id` |

## โครง docs/erd-readme.md (เขียนตามนี้เสมอ)

```markdown
# ERD — <ชื่อโปรเจกต์>
> คู่กับ docs/data-model.md · อัปเดตล่าสุด: <วันที่> · อ้างอิง: <data-model.md vX / migration ล่าสุด NNNN_*>

## วิธีดูแผนภาพ (ไม่ต้องรู้ technical)
1. เปิด https://dbdiagram.io/d ในเบราว์เซอร์
2. copy เนื้อหาไฟล์ `docs/erd.dbml` ทั้งหมดไปวางแทนโค้ดในช่องซ้าย
3. แผนภาพตาราง + เส้นความสัมพันธ์จะขึ้นทางขวา (ลากจัดตำแหน่งได้)

## สรุปโครงสร้างเป็นภาษาคน
- **<ตาราง>** — เก็บอะไร ผูกกับตารางไหน (1 บรรทัดต่อตาราง)

## สัญลักษณ์
เส้น `*` → `1` = หลายรายการชี้ไปของชิ้นเดียว (เช่น หลายคำสั่งซื้อเป็นของลูกค้าคนเดียว)
```

## ตรวจผล
เปิด https://dbdiagram.io/d → paste `docs/erd.dbml` → ต้องเห็น **เส้นเชื่อมระหว่างตาราง** (ไม่ใช่ตารางลอย ๆ) · ถ้าไม่มีเส้น = ขั้น 2 ไม่ได้รัน หรือ design ไม่มี FK

## เกี่ยวกับ skill อื่น
- **`skill-data-modeling`** กำหนดมาตรฐาน *design* (UUID v7, soft-delete, 4 คำถาม) — skill นี้ทำ *ภาพ* ให้ตรง design
- ใช้โดย **`subagent-data-architect`** เป็น deliverable บังคับ (กฎ 3 ไฟล์คู่กัน)
