# kissofbeauty — Kiss of Beauty Marketplace

Claude **plugin marketplace** ขององค์กร Kiss of Beauty (ดูแลโดยทีม BI)
รวม plugin · skill · subagent และมาตรฐานการทำงาน — ติดตั้งครั้งเดียว ใช้ได้ทุก project และอัปเดตต่อเนื่อง

> Kiss of Beauty's Claude plugin marketplace, maintained by the BI Team.

- **Marketplace:** `kissofbeauty`
- **Owner:** BI-Team · database@kissofbeauty.co.th

---

## 📦 Plugins ในนี้

| Plugin | รายละเอียด | Skills |
|---|---|---|
| [`devops`](plugins/devops) | DevOps & standards | `skill-git-standard` (Git/GitHub) · `skill-docker-standard` (containerization) · `skill-architecture-standard` (approved stack + UAT/prod topology) |
| [`management`](plugins/management) | PM & orchestration | `skill-PM` (discovery → Project Proposal) · `skill-init` (สร้าง skill ใหม่) |
| [`security`](plugins/security) | Security toolkit | `skill-cybersecurity` (OWASP code scan) · `-api` (API Top 10:2023) · `-llm` (LLM Top 10:2025) · `-supply-chain` (SCA/deps) · `-secret-scan` (secret + git history) · `-container-iac` (Docker/K8s/Terraform) · `-threat-model` (STRIDE) · **subagent** `subagent-cybersecurity-auditor` (full audit รวมทุกด้าน) · **command** `/security-check [path]` (สั่ง audit ทั้ง project) |
| [`developer`](plugins/developer) | Engineering team | `skill-frontend-web` · `skill-backend` · `skill-sql` · `skill-python` (venv-per-project) · `skill-fastapi` · `ui-ux-pro-max` (design intelligence) · `skill-software-testing` (test + UAT) · **subagents** `subagent-fullstack` (build per proposal) + `subagent-qa-tester` (test/UAT/security + PM-mediated fix loop) |

---

## 🗺️ โครงสร้าง skill & flow การทำงาน

marketplace แบ่งเป็น 4 plugin ตามบทบาท — **management** (วางแผน) · **devops** (มาตรฐานวิศวกรรม) · **security** (ความปลอดภัย) · **developer** (ทีม dev ลงมือทำ)

### โครงสร้าง skill ทั้งหมด

```
kob-claude-plugins  (marketplace: kissofbeauty)
│
├── management ──┬── skill-init ───────────── สร้างโครง skill ใหม่ (SKILL.md + README) ตามมาตรฐาน
│   (PM/วางแผน)  └── skill-PM ──────────────── main agent = PM: คุย user → 📄 Project Proposal
│                                            (Full/Lean) → ประเมิน stack/subagent → คุมให้ทำตาม requirement
│
├── devops ──────┬── skill-git-standard ───── มาตรฐาน git: main←uat←feature, credential gate, PR-only
│   (มาตรฐาน     ├── skill-docker-standard ── containerize: dev ด้วย compose, ไม่ฝัง cred ใน image,
│    วิศวกรรม)   │                            BI build จาก main → push registry (private)
│               └── skill-architecture-standard ── stack/เครื่องมือที่อนุมัติ + topology UAT/prod
│
├── security ────┬── skill-cybersecurity ──────────── สแกนโค้ด OWASP Top 10:2025
│   (ความ        ├── skill-cybersecurity-api ───────── OWASP API Top 10:2023
│    ปลอดภัย)    ├── skill-cybersecurity-llm ───────── OWASP LLM Top 10:2025
│               ├── skill-cybersecurity-supply-chain ─ SCA/deps/CVE
│               ├── skill-cybersecurity-secret-scan ── secret + git history
│               ├── skill-cybersecurity-container-iac ─ Docker/K8s/Terraform
│               ├── skill-cybersecurity-threat-model ─ STRIDE (design-level)
│               ├── 🤖 subagent-cybersecurity-auditor ─ รวมทุกด้าน → report เดียว
│               └── ⌘ /security-check ──────────────── สั่ง audit ทั้ง project
│
└── developer ───┬── skill-frontend-web ────── HTML/CSS/SCSS/Tailwind/JS/TS/React
    (ทีม dev)    ├── skill-backend ─────────── API/server design + controller/service/repository
                 ├── skill-sql ─────────────── schema/query/security/migration
                 ├── skill-python ──────────── PEP8/OOP/SOLID + venv แยกต่อ project
                 ├── skill-fastapi ─────────── FastAPI (data API / ML serving)
                 ├── ui-ux-pro-max ─────────── design intelligence → design-brief → Claude Design
                 ├── skill-software-testing ── test design + UAT + defect report
                 ├── 🤖 subagent-fullstack ─── build ตาม proposal (ใช้ coding skills ทั้งหมด)
                 └── 🤖 subagent-qa-tester ─── test + UAT + security → loop กลับ fullstack (ผ่าน PM)
```

### flow การทำงานจริง (วงจรทีม)

```
🧑 user ↔ skill-PM ──► 📄 Project Proposal
                          │
              ui-ux-pro-max ──► 📄 design-brief ──► 🧑 Claude Design ──► source code
                          │                                                  │
                          ▼                                                  ▼
                  subagent-fullstack ◄───────────────────────────── (เอา design มาต่อ)
                  (frontend/backend/sql/python · docker · git)
                          │  ส่งงาน
                          ▼
                  subagent-qa-tester  (test + UAT + /security-check)
                          │  เจอ defect
                          ▼
                  🧑 PM เคาะว่าต้องแก้ไหม ──► loop กลับ fullstack ──► จน qa ผ่าน ──► deploy
```

**อ่าน flow:**
1. **PM** (`skill-PM`) คุยกับ user กลั่นความต้องการ → **Project Proposal** (ปลายทางไม่จำเป็นต้องเป็น app)
2. ถ้าต้องสร้างของ → **ui-ux-pro-max** ออกแบบ design system แล้วเขียน **design-brief** ส่งให้ user ไปป้อน **Claude Design** → ได้ source code
3. **subagent-fullstack** เอา design มาต่อ + เขียน backend/data ตาม proposal (ใช้ skill มาตรฐาน devops/developer)
4. **subagent-qa-tester** ทดสอบ + ทำ UAT + ตรวจความปลอดภัย (`/security-check`) → เจอ defect ส่งกลับ
5. **PM** เป็นคนเคาะว่าต้องแก้ตาม qa ไหม (PM รู้ความต้องการ user สุด) → วน loop จน qa ผ่าน → BI promote ขึ้น prod

> ทุก stage ยึดมาตรฐาน: git (`skill-git-standard`) · container (`skill-docker-standard`) · stack (`skill-architecture-standard`) · security gate ก่อน deploy

---

## 🚀 วิธีใช้งาน (แยกตาม surface)

ปัจจุบัน skill เผยแพร่ **2 ช่องทาง** เพราะ Claude Code กับ claude.ai ใช้กลไกคนละแบบ:

### A) Claude Code (ดึงจาก repo นี้ตรง ๆ)

> ✅ **repo นี้เป็น public** — ใครก็ `marketplace add` + ติดตั้งได้เลย ไม่ต้องเป็น member ของ org (Claude Code ใช้ git ดึงตรง)
> (สิทธิ์ **เขียน/แก้** ยังจำกัดเฉพาะ collaborator/org — ดู `CONTRIBUTING.md`)

```bash
# 1. เพิ่ม marketplace — ใส่ได้ทั้ง 2 แบบ:
/plugin marketplace add Kissofbeauty/kob-claude-plugins              # แบบ owner/repo
/plugin marketplace add https://github.com/Kissofbeauty/kob-claude-plugins.git   # แบบ git URL เต็ม (copy จากปุ่ม Code บน GitHub)

# 2. ติดตั้ง plugin
/plugin install devops@kissofbeauty
```
- หลังติดตั้ง `skill-git-standard` จะถูกหยิบมาใช้อัตโนมัติเมื่อทำงานกับ git หรือเรียกตรง `/devops:skill-git-standard`
- **อัปเดต:** `/plugin marketplace update kissofbeauty` (ดึง commit ล่าสุดจาก git อัตโนมัติ)
- plugin **ไม่ตั้ง `version`** → ทุก commit บน `main` คือเวอร์ชันล่าสุด

> ❗ ถ้าขึ้น **"Repository not found"** = พิมพ์ชื่อ repo ผิด หรือ repo ยังไม่ถูกตั้งเป็น public (ตรวจ Settings → Visibility)

### B) claude.ai — chat / cowork / Projects
skill ตัวเดียวกันใช้บน claude.ai ได้ (รูปแบบ `SKILL.md` เป็น open format เดียวกัน) แต่ **ไม่ได้ดึงจาก GitHub** — **admin** ต้องอัปเข้า workspace:
- admin อัป/อัปเดต skill ที่ **`claude.ai/admin-settings/skills`** → provision เปิดให้สมาชิกทุกคนในองค์กรอัตโนมัติ
- แจกเฉพาะกลุ่ม: bundle skill เป็น plugin แล้ว assign ให้ group
- ใช้ได้เฉพาะ **สมาชิกใน Claude for Team workspace** (บัญชี personal นอก workspace ต้องเชิญเข้ามาก่อน)
- ⚠️ ปัจจุบัน publish เป็น **manual** — ยังไม่มี Admin API ให้ automate

> รายละเอียด/ข้อจำกัดทั้งหมด: ดู [`requirements.md`](requirements.md) §5.1 (distribution matrix) และ §8 (Spike S1)

---

## 🗂️ โครงสร้าง repo

```
.
├── .claude-plugin/marketplace.json   # สารบัญ marketplace
├── plugins/
│   └── devops/                       # plugin: devops
│       ├── .claude-plugin/plugin.json
│       └── skills/skill-git-standard/   (SKILL.md + references/ hooks/ templates/)
├── scripts/validate.py               # ตัวตรวจ manifest/skill (รันก่อนเปิด PR)
├── .github/workflows/validate.yml    # CI: รัน validate.py ทุก push/PR
├── CLAUDE.md                          # บริบทโปรเจกต์ (อ่านก่อนเริ่มงาน)
├── requirements.md                   # requirement + scope + การตัดสินใจ
├── CONTRIBUTING.md                   # วิธีเพิ่ม/แก้ plugin สำหรับ dev BI
└── README.md
```

---

## 📚 เอกสาร

| ไฟล์ | สำหรับ |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | บริบทโปรเจกต์ — อ่านก่อนเริ่มงานทุกครั้ง |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | **dev** ที่จะเพิ่ม/แก้ plugin · branch model · validation · governance |
| [`requirements.md`](requirements.md) | scope · มติการออกแบบ · distribution strategy |

---

## ➕ อยากเพิ่ม skill / plugin?

ดูขั้นตอนเต็มใน **[`CONTRIBUTING.md`](CONTRIBUTING.md)** โดยสรุป:
1. แตก branch `feature/<name>` จาก `main`
2. วางไฟล์ตามมาตรฐาน (skill → `plugins/<plugin>/skills/<name>/SKILL.md`)
3. รัน `python scripts/validate.py` ให้ผ่าน
4. เปิด PR → review โดยคน + security gate → merge
