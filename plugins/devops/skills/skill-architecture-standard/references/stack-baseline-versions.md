# Stack Baseline Versions — เวอร์ชันขั้นต่ำของ toolchain (ข้อมูล ณ 2026-11-25)

กำหนดว่าแต่ละชั้นของ Approved Toolchain **ใช้เวอร์ชันไหนเป็น default / ยอมรับได้ / ห้ามใช้** อิง release schedule + security advisory จากแหล่ง official (รายละเอียด CVE ดู `security-advisory-digest-2026.md` ใน security plugin — `plugins/security/skills/skill-cybersecurity/references/`)

> **หลักการ:** (1) ใช้ **LTS / supported line เท่านั้น** (2) ภายใน line ใช้ **patch ล่าสุด** เสมอ (3) runtime ที่ **EOL = ห้าม** ทุก environment รวม UAT (4) pin base image ด้วย tag เต็ม + digest
> **อัปเดตไฟล์นี้:** เดือนละครั้ง หรือเมื่อ line ใดเปลี่ยนสถานะ (LTS → Maintenance → EOL) · ใครแก้ให้เปลี่ยนวันที่หัวไฟล์ด้วย

---

## ตาราง baseline

| ชั้น | Default (โปรเจกต์ใหม่) | ยอมรับได้ (โปรเจกต์เดิม) | ❌ ห้าม (EOL / ไม่ได้ patch) | ขั้นต่ำที่ต้อง patch ถึง |
|---|---|---|---|---|
| **Node.js** | **26 LTS** (`node:26-alpine`) — เป็น LTS ตั้งแต่ 2026-10-28 | 24 (ถึง 2028-04) · 22 (ถึง 2027-04-30) | **20, 25 และต่ำกว่า** (EOL) | 26.13.1 · 24.22.3 · 22.23.5 |
| **Next.js** | **16.4.x** (Active LTS) | 15.5.x (Maintenance LTS) | ≤ 14.x | 16.4.5 · 15.5.29 + `sharp` ≥ 0.35.5 |
| **React** | ตามที่ Next.js ล็อกให้ | — | เวอร์ชันก่อน patch RSC typed-array RCE (ต.ค. 2026) | ตาม Next.js patched |
| **Python** | **3.14** (`python:3.14-slim`, bugfix branch) | 3.12 / 3.13 (security-only) · 3.15 ถ้า lib รองรับครบ | **≤ 3.10** (3.10 EOL 2026-10-01) | 3.14.10 · 3.13.18 · 3.12.16 · 3.11.18 |
| **FastAPI / Starlette** | FastAPI ล่าสุด (0.165.x) | — | Starlette < 1.3.1 | **Starlette ≥ 1.3.1** (ล่าสุด 1.10 — ทดสอบ middleware ก่อนอัป) |
| **PostgreSQL** | **17** (`postgres:17-alpine`) | 16 · 18 · 19 เมื่อออก 19.1 แล้ว | **≤ 14** (14 EOL 2026-11-12) | 18.7 · 17.12 · 16.16 · 15.20 |
| **Docker Engine / Desktop** | Engine 29.10.x · Desktop 4.86+ | — | Engine < 29.3.1 (AuthZ bypass) | 29.10.1 · Desktop 4.86.0 |
| **OpenSSL** (มากับ base image) | 3.5 LTS (ถึง 2030-04) | 4.0 (ถึง 2027-05) · 4.1 (ถึง 2027-11) | 3.0 · 1.1.1 · 3.4 · **3.6** (EOL 2026-11-01) | 3.5.10 · 4.0.4 · 4.1.1 |
| **CA bundle** | `ca-certificates` / `certifi` ที่ออกหลัง **2026-10-17** (eMudhra) | — | image ที่ไม่ได้ rebuild ตั้งแต่ก่อน 2026-10-17 | rebuild image |
| **Auth** | Microsoft Entra ID (Auth.js / MSAL) | — | auth ที่เขียนเอง · JWT ที่ไม่ตรวจ `iss` / `aud` | Authenticator บนมือถือเวอร์ชันล่าสุด (บังคับผ่าน MDM) |
| **npm / pnpm / uv** | npm ≥ 11.10 (`min-release-age`) · pnpm 10.16+ (`minimumReleaseAge`) · uv (`exclude-newer`) | — | CI ที่ใช้ npm classic token (revoke แล้ว) | cooldown ≥ 3 วัน + Trusted Publishing |

## Docker tag ที่แนะนำ (ตัวอย่าง)
```dockerfile
FROM node:26-alpine@sha256:<digest>        # ดู digest จริงที่ hub.docker.com/_/node
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
2. แก้ตัวอย่าง base image ใน `skill-docker-standard` / `skill-fastapi` / README template / `container-iac-checks.md`
3. แจ้งทีม: โปรเจกต์ที่ยังอยู่บน line เก่าต้องอัปก่อน promote prod (`/security-check` จะ flag เป็น High)

## รอบหน้า (ธ.ค. 2026) ที่ต้องดู
- PostgreSQL 19.1 ออกเมื่อไร → พิจารณาเลื่อน default จาก 17
- OpenSSL CVE-2026-121481 (CISA 9.8 แต่ OpenSSL ให้ Low, ยังไม่มี fix)
- Next.js security release ประจำเดือน ธ.ค.
