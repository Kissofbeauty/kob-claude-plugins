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
| [`devops`](plugins/devops) | DevOps toolkit | `skill-git-standard` (เพิ่ม Docker / SSL / CI/CD เร็ว ๆ นี้) |
| [`management`](plugins/management) | PM & orchestration | `skill-PM` (discovery → Project Proposal) · `skill-init` (สร้าง skill ใหม่) |
| [`security`](plugins/security) | Security toolkit | `skill-cybersecurity` (สแกนช่องโหว่ OWASP Top 10:2025 — รองรับทุกภาษา) |

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
