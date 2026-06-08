---
name: git-standard
description: Team Git/GitHub standards. Use whenever performing git work in ANY project — committing, pushing, branching, opening PRs, or merging to production. Enforces a custom 3-tier branch model (main ← uat ← z-feature/<name>), a CRITICAL pre-commit credential gate, Conventional Commit messages, and PR-only/protected main. Trigger on git/commit/push/branch/merge/PR requests, or "/git-standard".
---

# Git Standard

มาตรฐานการใช้งาน Git/GitHub ของทีม — ยึดตามนี้เสมอเมื่อทำงานกับ git ในทุกโปรเจกต์

> Apply these rules whenever doing git work. Details live in `references/`; templates in `templates/`. Load a file only when you need the depth.

---

## 🌳 Branch Model (3-tier) — กฎหลัก

```
main  (production)  ←──PR──  uat  ←──PR──  z-feature/<featureName>
```

- **`main`** = production. **PR เท่านั้น + protected** (ห้าม push ตรง — GitHub Branch Protection บังคับ)
- **`uat`** = UAT. แยกมาจาก `main`. ใช้ PR ตามธรรมเนียม (**ไม่บังคับ** ฝั่ง server)
- **`z-feature/<featureName>`** = dev. แยกมาจาก `uat`. ชื่อ kebab-case เช่น `z-feature/user-login`

**Promotion flow:**
1. `z-feature/*` แยกจาก `uat` → พัฒนา
2. dev เสร็จ → merge เข้า `uat` → ทดสอบบน UAT
3. UAT ผ่าน → **เปิด PR** `uat` → `main` (อย่า `git push origin main` ตรง — จะถูก GitHub ปฏิเสธ)

→ รายละเอียด: `references/BRANCHING.md`, `references/WORKFLOW.md`

---

## 🚨 กฎ CRITICAL: ตรวจ Credential ก่อน Commit ทุกครั้ง

**ก่อนจะ commit เสมอ** ให้สแกนไฟล์ที่จะ commit ว่ามี credential หลุดเข้าไปไหม
(private key, AWS/Google/Slack/GitHub token, JWT/Bearer, hardcoded `password`/`api_key`/`secret`)

- **พบ → หยุดทันที แจ้งเตือนระดับ `CRITICAL`** พร้อม `file:line` และ **ห้าม commit** จนกว่าจะเคลียร์
- เตือน user ว่าถ้า key เคยหลุด/push ไปแล้ว ต้อง **revoke + rotate key** (ลบไฟล์เฉย ๆ ไม่พอ เพราะอยู่ใน history)
- บังคับอัตโนมัติด้วย hook ใน `hooks/pre-commit` — ติดตั้งใน repo ปลายทาง: `git config core.hooksPath hooks`
- ข้ามได้เฉพาะกรณี false positive ที่ user ยืนยัน: `git commit --no-verify`

→ รายละเอียด: `references/SECURITY.md`

---

## ✍️ Commit Message — Conventional Commits

รูปแบบ: `<type>(<scope>): <subject>` — type: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert`
subject เป็นคำสั่ง/ตัวพิมพ์เล็ก/ไม่เกิน ~50 ตัว/ไม่มีจุดท้าย เช่น `feat(auth): add Google OAuth login`

→ รายละเอียด: `references/COMMIT_CONVENTION.md`

---

## 🚦 Push Rules (สรุป)

1. ❌ ห้าม push ตรงเข้า `main` (บังคับ) — ผ่าน PR เสมอ
2. ✅ push เฉพาะ `z-feature/*` ของตัวเอง
3. ⚠️ force ได้เฉพาะ branch ตัวเอง และใช้ `--force-with-lease`
4. 🔄 pull/rebase ก่อน push เสมอ
5. 🧪 รัน test/lint ก่อน push
6. 🚨 credential gate ต้องผ่าน (ดูด้านบน)

---

## ⚙️ Setup repo ปลายทางให้ตรงมาตรฐาน

ก๊อปไฟล์จาก `templates/` ไปไว้ที่ root ของ repo จริง แล้วตั้งค่า:

```bash
git config commit.template .gitmessage   # ใช้ commit template
git config core.hooksPath hooks          # เปิด credential pre-commit gate
```

ไฟล์ใน `templates/`:
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `.gitmessage` | commit message template |
| `.gitattributes` | normalize line endings (CRLF/LF) |
| `gitignore` | rename เป็น `.gitignore` — กัน secret/build/OS junk |
| `github/PULL_REQUEST_TEMPLATE.md` | PR template (วางใน `.github/`) |
| `github/ISSUE_TEMPLATE/*` | bug/feature issue templates |

---

## 📚 Reference files (โหลดเมื่อต้องการรายละเอียด)

| ไฟล์ | เนื้อหา |
|---|---|
| `references/BRANCHING.md` | branch model, flow diagram, naming, merge rules, hotfix |
| `references/WORKFLOW.md` | ขั้นตอนทำงานประจำวัน, push rules, แก้ conflict, pre-PR checklist |
| `references/COMMIT_CONVENTION.md` | รูปแบบ commit message เต็ม |
| `references/SECURITY.md` | กฎ credential gate, รายการ secret, วิธีติดตั้ง hook |
| `references/GIT_GUIDE.md` | cheatsheet คำสั่ง git พื้นฐาน → ขั้นสูง |
| `hooks/pre-commit` | สคริปต์สแกน credential (ติดตั้งใน repo จริงด้วย `core.hooksPath`) |
