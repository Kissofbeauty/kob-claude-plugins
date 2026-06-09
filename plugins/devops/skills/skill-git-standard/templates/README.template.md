<!--
  README template — ตามมาตรฐาน skill-git-standard
  ต้องมี 2 ส่วน: (1) คำอธิบาย project  (2) Technical Information
  เติมเนื้อหาให้ครบ ลบคอมเมนต์/วงเล็บ <...> ออกเมื่อกรอกเสร็จ
-->

# <ชื่อโปรเจกต์ / Project Name>

<อธิบายสั้น ๆ ว่าโปรเจกต์นี้คืออะไร ทำอะไร แก้ปัญหาอะไรให้ใคร / one-paragraph summary>

## ✨ Features
- <ฟีเจอร์หลัก 1>
- <ฟีเจอร์หลัก 2>

## 🚀 Getting Started
```bash
# วิธีติดตั้งและรันแบบเร็วที่สุด / quickest way to run
<install command>
<run command>
```

---

# 🔧 Technical Information

> ข้อมูลทางเทคนิคทั้งหมดที่ dev ควรรู้เพื่อทำงานกับโปรเจกต์นี้ได้
> (เป้าหมาย: dev ใหม่อ่านจบแล้วเริ่มงานต่อได้เองโดยไม่ต้องถาม)

## Tech Stack
- **Language/Runtime:** <เช่น Python 3.12 / Node 20>
- **Framework:** <เช่น FastAPI / Next.js>
- **Database:** <เช่น PostgreSQL 16>
- **Key libraries:** <รายการสำคัญ + เวอร์ชัน>

## Project Structure
```
<โครงสร้างโฟลเดอร์หลัก พร้อมคำอธิบายสั้น ๆ ว่าแต่ละส่วนทำอะไร>
src/
  ...
```

## Setup & Run
```bash
# 1. ติดตั้ง dependencies
<...>
# 2. ตั้งค่า environment
cp .env.example .env   # แล้วแก้ค่าให้ครบ
# 3. รัน / build / test
<run>      # dev server
<build>    # production build
<test>     # run tests
```

## Environment Variables
| ตัวแปร (Var) | จำเป็น | คำอธิบาย / ค่า ตัวอย่าง |
|---|---|---|
| `<VAR_NAME>` | ✅ | <อธิบาย — อย่าใส่ค่าจริง/secret ลง README> |

## Database / External Services
- **Schema / migration:** <วิธี migrate, ที่อยู่ schema>
- **External APIs / services:** <บริการที่เชื่อมต่อ + จุดประสงค์>

## Architecture / Data Flow
<ภาพรวมการทำงาน, request flow, decision สำคัญ — diagram ได้ยิ่งดี>

## Deployment
- **Environments:** `main` → Production · `uat` → UAT  (ดู branch model ของทีม)
- **วิธี deploy:** <CI/CD pipeline, manual steps, ที่ deploy>

## Conventions & Gotchas
- ใช้ Git ตามมาตรฐานทีม: branch model `main ← uat ← feature/<name>`, Conventional Commits, ห้าม commit secret
- <ข้อตกลงเฉพาะโปรเจกต์ / จุดที่พลาดบ่อย / สิ่งที่ต้องระวัง>
