---
name: skill-architecture-standard
description: Team architecture & approved-toolchain standard. Use when starting a project, choosing a stack, writing the "Proposed Approach" of a proposal, or deciding what tools/services/hosting to use. Defines the org's default stack, deploy topology (UAT=Hostinger, prod=AWS), and a decision guide by app type. Trigger on "architecture", "tech stack", "ใช้เครื่องมืออะไร", "วางสถาปัตยกรรม", "เลือก stack", or "/skill-architecture-standard".
allowed-tools: Read, Glob, Grep, Write, Edit
---

# skill-architecture-standard — Architecture & Approved Toolchain

มาตรฐานว่า **โปรเจกต์ขององค์กรใช้ stack/เครื่องมือ/โครง deploy อะไร** — ยึดเป็น default · เบี่ยงได้แต่ต้องมีเหตุผล — **ก่อนถึง phase ขึ้น production: PM เคาะได้เลย** · BI review ตอน promote ขึ้น prod

> ใช้คู่กับ `skill-PM` (เขียน "Proposed Approach/Resources" ใน proposal อ้าง skill นี้) · บังคับด้วย `skill-git-standard` + `skill-docker-standard` + security plugin

---

## 🧰 Approved Toolchain (default)

| ชั้น | มาตรฐาน | หมายเหตุ |
|---|---|---|
| **App (web)** | **Next.js** | FE+BE ในตัว · default สำหรับ web/webapp |
| **API** | Next.js API routes (เล็ก) · FastAPI (Python/data) | เลือกตามทีม/โหลด |
| **AI/LLM** | Claude API + MCP | ตรวจด้วย `skill-cybersecurity-llm` |
| **Data** | **PostgreSQL self-host ใน Docker (compose)** — default ทุก environment | **RDS (managed)** เฉพาะเมื่อ**ทีม BI ร้องขอ**ใน phase production (โอกาสน้อย — ต้นทุนสูง) |
| **Auth** | **Microsoft Authentication — Microsoft Entra ID** (บัญชีองค์กร, OIDC/OAuth 2.0) · Next.js ใช้ Auth.js provider `microsoft-entra-id` หรือ MSAL · FastAPI verify JWT ของ Entra (JWKS) | ❌ ห้าม hand-roll auth · app registration / client secret ขอผ่าน BI (เก็บใน secret manager เท่านั้น) |
| **Container** | **Docker + compose** | ตาม `skill-docker-standard` |
| **Source/CI** | **GitHub** + CI/CD | ตาม `skill-git-standard` (main←uat←feature) |
| **Security gate** | security plugin + **`/security-check`** | ก่อน promote prod |
| **Runtime baseline** | **Node 24 LTS** (→ 26 หลัง 2026-10-28) · **Next.js 16.4.x** · **Python 3.14** · **PostgreSQL 17** · Docker Engine 29.9+ | ห้าม line ที่ EOL (Node 20, Python ≤3.10, PostgreSQL ≤14) — ดู `references/stack-baseline-versions.md` |

## 🌐 Deploy Topology (สำคัญ)
```
dev local (docker compose)
      │  push source → GitHub (skill-git-standard)
      ▼
UAT = Hostinger (VPS + Docker)     ← ทีมทั่วไป deploy/ทดสอบที่นี่
      │  management approve (บน main)
      ▼
Prod = AWS (App Runner / Lightsail Containers)  ← BI promote เท่านั้น
      ▲ image เดียวกัน (Docker parity) · official image build จาก main โดย BI
```

## 🧭 Decision Guide — เลือกใช้ตามชนิดงาน
| ชนิดงาน | ใช้ |
|---|---|
| Web / webapp | Next.js + Postgres + Docker compose |
| API / data service | FastAPI (Python) หรือ Next API + Postgres |
| AI / LLM / agent | Claude API + MCP (+ ตรวจ `skill-cybersecurity-llm`) |
| Static / landing | static build (ไม่บังคับ compose) |
| มี backend ที่รันบน server | **ต้อง** containerize (`skill-docker-standard`) |

---

## Rules
- **ใช้ default ก่อนเสมอ** — เบี่ยงจากมาตรฐานต้องมีเหตุผลชัด + ระบุใน "Proposed Approach" ของ proposal · **ก่อน production: PM เคาะได้เลยไม่ต้องถาม BI** · BI review ตอน promote prod
- ทุกแอป server-side → Docker + GitHub + ผ่าน security gate ก่อน prod
- **ใช้ LTS/supported line + patch ล่าสุดเสมอ** — runtime ที่ EOL ห้ามทุก env (รวม UAT) · `/security-check` จะ flag เป็น High · baseline ใน `references/stack-baseline-versions.md` (BI refresh เดือนละครั้ง)
- prod อยู่ AWS · UAT อยู่ Hostinger · **BI เท่านั้น promote ขึ้น prod**
- DB default = **self-host PostgreSQL ใน Docker** ทุก env · **RDS เฉพาะเมื่อทีม BI ร้องขอตอน production** — ❌ ห้าม hand-roll auth (auth ใช้ **Microsoft Entra ID**) · ❌ ทีมทั่วไปไม่แตะ AWS เอง (รวมศูนย์ที่ BI — กัน cost/security)

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/toolchain-and-topology.md` | รายละเอียด stack แต่ละชั้น + เหตุผล + topology UAT/prod + cost/security guardrails |
| `references/stack-baseline-versions.md` | เวอร์ชัน default / ยอมรับได้ / ห้าม ของทุกชั้น + Docker tag + วิธีเช็ค (อิง advisory digest ของ security plugin) |
