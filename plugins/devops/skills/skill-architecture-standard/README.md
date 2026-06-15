# skill-architecture-standard

## Overview
มาตรฐานสถาปัตยกรรม + toolchain ที่องค์กรอนุมัติให้ใช้ — กำหนด default stack (app/data/auth/container), โครง deploy (UAT=Hostinger, prod=AWS), และ decision guide ว่างานชนิดไหนใช้อะไร เพื่อให้ทุกโปรเจกต์ (รวม hackathon) เลือกเครื่องมือไปในทิศทางเดียวกัน

## วิธีการคิดและการทำงานของ Skill
1. **กำหนด default toolchain** — Next.js · managed Postgres · managed Auth · Docker · GitHub · security gate
2. **Topology ชัด** — dev (compose) → UAT (Hostinger) → prod (AWS, BI promote เท่านั้น) ด้วย Docker parity
3. **Decision guide** — web/API/AI/static เลือกอะไร + กฎ "เบี่ยงต้องมีเหตุผล + ถาม architect/BI"
4. **ผูกกับ skill อื่น** — skill-PM อ้างตอนเขียน proposal · บังคับด้วย git-standard + docker-standard + security plugin

## ผลลัพธ์ที่ได้จากการใช้งาน
- ทีมรู้ทันทีว่า "ใช้เครื่องมืออะไร" โดยไม่ต้องเดา/ถามทุกครั้ง
- สถาปัตยกรรม + deploy เป็นมาตรฐานเดียว (parity, รวมศูนย์ prod ที่ BI)
- ลดความเสี่ยง cost/security จากการเลือก stack มั่ว

## วิธีใช้
```
/skill-architecture-standard          # เมื่อเริ่มโปรเจกต์ / เลือก stack / เขียน proposed approach
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อพูดถึง architecture/tech stack/"ใช้เครื่องมืออะไร"

## ตัวอย่าง
```
user: "จะเริ่มทำ webapp ใหม่ ใช้อะไรดี"
→ skill ตอบ default: Next.js + managed Postgres + Docker compose + GitHub,
  deploy UAT Hostinger → BI promote AWS, ผ่าน /security-check ก่อน prod
```
