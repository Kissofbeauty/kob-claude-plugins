# Mixovage Marketplace

Claude Code **plugin marketplace** ของทีม — รวม plugin และมาตรฐานการทำงาน
ติดตั้งครั้งเดียว ใช้ได้ทุก project และอัปเดตตามอัตโนมัติ

> A Claude Code plugin marketplace. Install once, use across all projects, auto-updates.

---

## 📦 Plugins ในนี้

| Plugin | รายละเอียด | Skills |
|---|---|---|
| [`devops`](plugins/devops) | DevOps toolkit | `git-standard` (เพิ่ม Docker / SSL / CI/CD เร็ว ๆ นี้) |

---

## 🚀 วิธีติดตั้ง (สำหรับ teammate)

ใน Claude Code:

```bash
# 1. เพิ่ม marketplace (ใช้ชื่อ owner/repo บน GitHub)
/plugin marketplace add <your-org>/<this-repo>

# 2. ติดตั้ง plugin devops (ใช้ชื่อ marketplace = mixovage-marketplace)
/plugin install devops@mixovage-marketplace
```

> หลังติดตั้ง skill `git-standard` จะถูกหยิบมาใช้อัตโนมัติเมื่อทำงานกับ git
> (commit / push / branch / merge / PR) หรือเรียกตรงด้วย `/devops:git-standard`

### อัปเดตเป็นเวอร์ชันล่าสุด
```bash
/plugin marketplace update mixovage-marketplace
```
plugin นี้**ไม่ตั้ง `version`** ในมanifest → ทุก commit ใหม่ถือเป็นเวอร์ชันล่าสุด (auto-update)

---

## 🗂️ โครงสร้าง repo

```
.
├── .claude-plugin/
│   └── marketplace.json              # สารบัญ marketplace
├── plugins/
│   └── devops/                       # plugin: devops
│       ├── .claude-plugin/
│       │   └── plugin.json           # manifest ของ plugin
│       └── skills/
│           └── git-standard/         # skill: git-standard
│               ├── SKILL.md
│               ├── references/        # เอกสารมาตรฐานเต็ม
│               ├── hooks/             # pre-commit credential scanner
│               └── templates/         # .gitmessage, .gitignore, PR/issue templates
├── .gitignore
└── README.md
```

---

## ➕ เพิ่ม skill / plugin ใหม่ในอนาคต

- **เพิ่ม skill ใน devops:** สร้างโฟลเดอร์ใหม่ใต้ `plugins/devops/skills/<skill-name>/` พร้อม `SKILL.md`
- **เพิ่ม subagent:** สร้าง `plugins/devops/agents/<name>.md` (อย่าลืมใส่ `Skill` ใน tools ถ้าต้องเรียก skill)
- **เพิ่ม plugin ใหม่ (เช่น `qa`, `pm`):** สร้าง `plugins/<name>/` แล้วเพิ่ม entry ใน `marketplace.json`
