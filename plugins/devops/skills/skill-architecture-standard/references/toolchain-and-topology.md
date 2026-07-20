# Toolchain & Topology — รายละเอียด + เหตุผล

## เหตุผลของแต่ละมาตรฐาน
- **Next.js (web default):** FE+BE ในตัว, Claude เขียนเก่ง, deploy เป็น container ง่าย, ลดจำนวน stack ที่ทีมต้องรู้
- **managed Postgres:** Neon/Supabase (dev/UAT) ฟรี/เร็ว, RDS (prod) ที่ BI ดูแล — ไม่ต้อง self-host (กัน ops/security พลาด) · Postgres เหมือนกันทุก env = parity
- **managed Auth (Supabase/Clerk):** auth เขียนเองพลาดง่าย + เสี่ยง (ดู OWASP A07) → ใช้ของสำเร็จ
- **Docker + compose:** dev = prod parity, BI promote image เดียวข้าม Hostinger→AWS ได้
- **GitHub + 3-tier:** main←uat←feature, PR-only, credential gate (skill-git-standard)

## Topology รายละเอียด
| Env | ที่ | ใคร deploy | how |
|---|---|---|---|
| dev | local | ทุกคน | `docker compose up --build` |
| UAT | Hostinger (VPS+Docker) | ทีมทั่วไป (self-serve) | push source → CI build → run container |
| prod | AWS (App Runner / Lightsail Containers) | **BI เท่านั้น** | CI build official image จาก main → Docker Hub private → deploy |

> เลือก App Runner = auto-scale+HTTPS · Lightsail Containers = ราคาคงที่ (กัน cost บาน hackathon)

## Guardrails (cost + security)
- **AWS รวมศูนย์ที่ BI** — ทีมทั่วไปไม่เปิด account/resource เอง · ตั้ง Budget + Alert
- **Docker Hub = private** (BI ดูแล) · credential ของ registry/cloud อยู่ใน CI secret เท่านั้น
- **`/security-check` ก่อน promote** — secret-scan + container-iac + OWASP ตามชนิดงาน
- **Docker parity บังคับ** — UAT กับ prod ต้องเป็น image เดียวกัน

## เมื่อจะเบี่ยงจากมาตรฐาน
1. ระบุเหตุผลใน "Proposed Approach" ของ project-proposal (skill-PM)
2. **ก่อนถึง phase ขึ้น production → PM เคาะได้เลย** (ไม่ต้องรอ BI) · ตอน promote ขึ้น prod → BI review อีกชั้นตาม guardrails
3. ถ้า approve → บันทึกเป็น decision ใน CLAUDE.md/requirements ของโปรเจกต์นั้น
