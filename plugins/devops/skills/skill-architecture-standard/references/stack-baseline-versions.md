# Stack Baseline Versions — เวอร์ชันขั้นต่ำของ toolchain (ข้อมูล ณ 2026-10-24)

กำหนดว่าแต่ละชั้นของ Approved Toolchain **ใช้เวอร์ชันไหนเป็น default / ยอมรับได้ / ห้ามใช้** อิง release schedule + security advisory จากแหล่ง official (รายละเอียด CVE ดู `security-advisory-digest-2026.md` ใน security plugin — `plugins/security/skills/skill-cybersecurity/references/`)

> **หลักการ:** (1) ใช้ **LTS / supported line เท่านั้น** (2) ภายใน line ใช้ **patch ล่าสุด** เสมอ (3) runtime ที่ **EOL = ห้าม** ทุก environment รวม UAT (4) pin base image ด้วย tag เต็ม + digest
> **อัปเดตไฟล์นี้:** เดือนละครั้ง หรือเมื่อ line ใดเปลี่ยนสถานะ (LTS → Maintenance → EOL) · ใครแก้ให้เปลี่ยนวันที่หัวไฟล์ด้วย

---

## ตาราง baseline

| ชั้น | Default (โปรเจกต์ใหม่) | ยอมรับได้ (โปรเจกต์เดิม) | ❌ ห้าม (EOL / ไม่ได้ patch) | ขั้นต่ำที่ต้อง patch ถึง |
|---|---|---|---|---|
| **Node.js** | **24 LTS** (`node:24-alpine`) → ย้ายเป็น **26** หลัง 26 เป็น LTS **2026-10-28** | 22 (Maintenance ถึง 2027-04-30) | **20 และต่ำกว่า** (EOL 2026-04-30) | 26.12.1 · 24.22.1 · 22.23.4 |
| **Next.js** | **16.4.x** (Active LTS) | 15.5.x (Maintenance LTS) | ≤ 14.x | 16.4.1 · 15.5.28 + `sharp` ≥ 0.35.5 |
| **React** | ตามที่ Next.js ล็อกให้ | — | เวอร์ชันก่อน patch React2Shell (ธ.ค. 2025) | ตาม Next.js patched |
| **Python** | **3.14** (`python:3.14-slim`, bugfix branch) | 3.12 / 3.13 (security-only) · 3.15 ถ้า lib รองรับครบ | **≤ 3.10** (3.10 EOL 2026-10-01) | 3.14.9 · 3.13.17 · 3.12.15 · 3.11.17 |
| **FastAPI / Starlette** | FastAPI ล่าสุด (0.162.x) | — | Starlette < 1.0.1 | **Starlette ≥ 1.3.1** |
| **PostgreSQL** | **17** (`postgres:17-alpine`) | 16 · 18 | **≤ 14** (14 EOL 2026-11-12) · ≤ 13 EOL แล้ว | 18.6 · 17.11 · 16.15 |
| **Docker Engine / Desktop** | Engine 29.9.x · Desktop 4.86+ | — | Engine < 29.3.1 (AuthZ bypass) | 29.9.2 · Desktop 4.86.0 |
| **OpenSSL** (มากับ base image) | 3.5 LTS (ถึง 2030-04) | 3.6 (EOL 2026-11-01) → ต้องย้าย | 3.0 · 1.1.1 · 3.4 (EOL 2026-10-22) | 3.5.9 |
| **CA bundle** | `ca-certificates` / `certifi` ที่ออกหลัง **2026-10-17** (eMudhra) | — | image ที่ไม่ได้ rebuild ตั้งแต่ก่อน 2026-10-17 | rebuild image |
| **npm / pnpm** | npm ≥ 11.10 (`min-release-age`) · pnpm 10.16+ (`minimumReleaseAge`) | — | CI ที่ใช้ npm classic token (revoke แล้ว) | cooldown ≥ 3 วัน + Trusted Publishing |

## Docker tag ที่แนะนำ (ตัวอย่าง)
```dockerfile
FROM node:24-alpine@sha256:<digest>        # ดู digest จริงที่ hub.docker.com/_/node
FROM python:3.14-slim@sha256:<digest>
# compose: image: postgres:17-alpine
```

## วิธีเช็คในโปรเจกต์
```bash
node -v && npm -v                       # ต้อง ≥ baseline ข้างบน
npx next --version                      # หรือดู package-lock.json → "node_modules/next"
python -V && pip show starlette fastapi # Starlette ≥ 1.3.1
docker version --format '{{.Server.Version}}'
docker compose exec db postgres --version
```

## เมื่อ line เปลี่ยนสถานะ (checklist สำหรับ BI)
1. อัปเดตตารางนี้ + `security-advisory-digest-2026.md`
2. แก้ตัวอย่าง base image ใน `skill-docker-standard` / `skill-fastapi` / README template
3. แจ้งทีม: โปรเจกต์ที่ยังอยู่บน line เก่าต้องอัปก่อน promote prod (`/security-check` จะ flag เป็น High)
