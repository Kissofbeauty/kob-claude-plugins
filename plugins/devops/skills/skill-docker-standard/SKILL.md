---
name: skill-docker-standard
description: Team Docker/containerization standard. Use whenever building, running, or deploying an app with containers — Dockerfile, docker compose, image build, registry, or "ขึ้น server/deploy". Enforces a 2-role model (everyone develops locally with docker compose; only BI pushes the official image), a strict no-credentials-in-image rule, and a build-from-main CI/CD flow. Trigger on docker/dockerfile/compose/containerize/deploy requests, or "/skill-docker-standard".
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# skill-docker-standard — Team Containerization Standard

มาตรฐานการ containerize ของทีม — **ยึดตามนี้เสมอ**เมื่อแอปต้องรันบน server

> หลักการ: **โค้ดทุกอย่างที่รันบน server ต้องอยู่ใน container** · dev เหมือน prod (parity) · **secret ไม่อยู่ใน image เด็ดขาด**

---

## 👥 2 บทบาท (สำคัญ — ทำตามให้ถูกกลุ่ม)

```
ทุกคน (รวมทีม hackathon / dev ทั่วไป)            BI เท่านั้น (หลัง management approve)
──────────────────────────────────────          ──────────────────────────────────
• dev local ด้วย docker compose                  • CI build "official image" จาก main
• build image ใน local ไว้ทดสอบ                   • push → Docker Hub (private repo)
• source → GitHub (skill-git-standard)            • ต่อ CI/CD: main เปลี่ยน → rebuild → deploy prod
❌ ห้าม push image ขึ้น registry
❌ ห้ามใส่ credential ใน image
```

> 🔑 **official image (ตัวขึ้น prod) เกิดจาก CI build จาก `main` ที่ approve แล้วเท่านั้น** — ไม่เอา image จากเครื่อง user มา push (เพื่อ reproducible + ตรวจสอบได้)

---

## 🟢 สำหรับ "ทุกคน" — Develop ด้วย Docker Compose

**กฎ:** ถ้าแอปต้องรันบน server (web/webapp/API/มี backend) → **ต้องมี `Dockerfile` + `docker-compose.yml`** ตั้งแต่ต้น
(static ล้วน ไม่มี backend → ไม่บังคับ compose แต่แนะนำ container เพื่อ parity)

ขั้นตอน:
1. เขียน `Dockerfile` (multi-stage, non-root) — ดู `references/dockerfile-compose-guide.md`
2. เขียน `docker-compose.yml` รวม service ที่ต้องใช้ (app + db + ฯลฯ) สำหรับ dev local
3. รัน local: `docker compose up --build` → ทดสอบให้ผ่านในกล่อง container
4. **secret** ใส่ผ่าน `env_file: .env` (gitignored) — **ไม่ hardcode, ไม่ COPY .env เข้า image**
5. push **source code** ขึ้น GitHub ตาม **`skill-git-standard`** (ไม่ push image)

---

## 🚫 กฎเหล็ก: ห้าม Credential ใน Image (per security)

| ❌ ห้าม | ✅ ทำแทน |
|---|---|
| `ENV API_KEY=xxx` / `COPY .env .` ใน Dockerfile | inject ตอน runtime: `env_file` / `-e` / orchestrator secret |
| hardcode key/password ในโค้ดที่ถูก build เข้า image | อ่านจาก env var ตอนรัน |
| build-arg ที่เป็น secret แล้วค้างใน layer | ใช้ **multi-stage** หรือ `--secret` mount (BuildKit) |

- ต้องมี **`.dockerignore`** ครอบ `.env`, `*.pem`, `secrets*`, `.git`
- ก่อน promote ขึ้น prod → รัน **`/skill-cybersecurity-container-iac`** + **secret-scan** (security plugin) ให้ผ่าน
> หลุด credential เข้า image = ถือว่ารั่ว (image ถูกดึงไปแตก layer ดูได้) → ต้อง revoke/rotate

→ รายละเอียด: `references/dockerfile-compose-guide.md`

---

## 🔵 สำหรับ "BI เท่านั้น" — Promote ขึ้น Production

ทำ**หลัง management approve** เท่านั้น:
1. ยืนยันว่า source อยู่บน `main` (ผ่าน PR + review + security gate ตาม skill-git-standard)
2. **CI/CD build official image จาก `main`** (ไม่ใช่จาก local) → tag ด้วย commit-sha + `prod`
3. push → **Docker Hub (private repo)** ที่ทีม BI ดูแล (credential ของ registry อยู่ใน CI secret — ไม่อยู่ใน image)
4. ต่อ CI/CD: ทุกครั้งที่ `main` เปลี่ยน → rebuild → update image → deploy prod (AWS)

→ รายละเอียด CI/CD + การ promote: `references/cicd-and-promote.md`

---

## 🔗 End-to-End Flow
```
dev local (compose) ──push source──► GitHub (skill-git-standard)
        │                                   │
        │                              management approve (บน main)
        │                                   ▼
        │                         BI: CI build image จาก main
        │                                   ▼
        └─ ทดสอบใน container       Docker Hub (private) ──► deploy prod (AWS)
                                   ▲ secret มาจาก CI/runtime ไม่อยู่ใน image
```

## เช็กก่อนปิดงาน
1. แอป server-side มี `Dockerfile` + `docker-compose.yml` + `.dockerignore` ครบ
2. รัน `docker compose up --build` ผ่านใน local
3. **ไม่มี credential ใน image/Dockerfile** (ผ่าน container-iac + secret-scan)
4. source ขึ้น GitHub ตาม skill-git-standard (ไม่ push image — ยกเว้น BI หลัง approve)

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/dockerfile-compose-guide.md` | Dockerfile (multi-stage/non-root) + compose + no-secret patterns |
| `references/cicd-and-promote.md` | (BI) CI/CD build-from-main → Docker Hub private → deploy prod |
