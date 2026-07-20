---
name: skill-git-standard
description: Team Git/GitHub standards. Use whenever performing git work in ANY project — committing, pushing, branching, opening PRs, or merging to production. Enforces a custom 3-tier branch model (main ← uat ← feature/<name>), a CRITICAL pre-commit credential gate, Conventional Commit messages, PR-only/protected main, and a mandatory README.md (project description + Technical Information). Trigger on git/commit/push/branch/merge/PR requests, or "/skill-git-standard".
---

# Git Standard

มาตรฐานการใช้งาน Git/GitHub ของทีม — ยึดตามนี้เสมอเมื่อทำงานกับ git ในทุกโปรเจกต์

> Apply these rules whenever doing git work. Details live in `references/`; templates in `templates/`. Load a file only when you need the depth.

---

## 🌳 Branch Model (3-tier) — กฎหลัก

```
main  (production)  ←──PR──  uat  ←──PR──  feature/<featureName>
```

- **`main`** = production. **PR เท่านั้น + protected** (ห้าม push ตรง — GitHub Branch Protection บังคับ)
- **`uat`** = UAT. แยกมาจาก `main`. ใช้ PR ตามธรรมเนียม (**ไม่บังคับ** ฝั่ง server)
- **`feature/<featureName>`** = dev. แยกมาจาก `uat`. ชื่อ kebab-case เช่น `feature/user-login`

**Promotion flow:**
1. `feature/*` แยกจาก `uat` → พัฒนา
2. dev เสร็จ → merge เข้า `uat` → ทดสอบบน UAT
3. UAT ผ่าน → **เปิด PR** `uat` → `main` (อย่า `git push origin main` ตรง — จะถูก GitHub ปฏิเสธ)

→ รายละเอียด: `references/BRANCHING.md`, `references/WORKFLOW.md`

---

## 🚧 กฎเหล็ก: ห้าม PR ข้าม UAT + ใครเปิด PR ขั้นไหน

> มาจากความผิดพลาดจริง: PR feature เผลอตั้ง base เป็น `main` (GitHub default) → merge ข้าม uat เข้า prod ตรง ๆ โดยไม่ได้ทดสอบ

### 1) ❌ ห้ามข้าม UAT — ทุกการเปลี่ยนแปลงต้องผ่าน `uat` ก่อนเสมอ
- PR ของ `feature/*` **base ต้องเป็น `uat` เท่านั้น** — **ห้าม** `feature/* → main` เด็ดขาด
- ก่อนกด/แนะนำ merge PR ใด ๆ ที่ base = `main` → **เช็กก่อนว่า head เป็น `uat` ไหม** ถ้าไม่ใช่ `uat` (เช่นเป็น feature) → **หยุด เตือน user ทันที** ว่ากำลังจะข้าม UAT
- ลำดับเดียวที่ยอมรับ: `feature/* → uat` (ทดสอบ) → `uat → main` (เผยแพร่)

#### 🔗 กฎลิงก์เปิด PR — ฝัง base=uat + title + description มาในลิงก์เสมอ (กันพลาดถาวร)
> เวลาเสนอลิงก์ให้ user เปิด PR ของ feature **ห้ามใช้** ลิงก์แบบ `…/pull/new/<branch>` — เพราะมันตั้ง base เป็น default branch (`main`) เสมอ → หลุดข้าม uat ง่าย

- **ใช้ฟอร์แมต compare ที่ระบุ base + กรอก title/body มาในตัวลิงก์เลย:**
  ```
  https://github.com/<org>/<repo>/compare/uat...<feature-branch>?expand=1&title=<TITLE>&body=<BODY>
  ```
  - `uat...<branch>` → **ตัวหน้า = base = `uat`** · ตัวหลัง = compare (feature) · ลำดับห้ามสลับ
  - `?expand=1` → เปิดฟอร์ม PR ให้ทันที
  - `&title=<TITLE>` → เติม PR title (ใช้ Conventional Commit เช่น `feat(scope): ...`)
  - `&body=<BODY>` → เติม PR description ให้พร้อม
  - ผลคือหน้า PR ขึ้น **base: uat + title + description กรอกมาให้แล้ว** user แค่กด Create
- **ต้อง URL-encode** ค่า title/body เสมอ (เว้นวรรค→`%20`, ขึ้นบรรทัด→`%0A`, `#`→`%23`, `&`→`%26`) — ไม่งั้นลิงก์เพี้ยน
- **description ที่ฝัง ต้องเขียนทุกครั้ง** — สรุปสั้น ๆ ว่า PR นี้ทำอะไร/แก้อะไร/กระทบอะไร (อย่าปล่อยว่าง)
- ถ้าจำเป็นต้องใช้หน้า GitHub ที่ base เป็น `main` อยู่ → **ย้ำ user ให้เปลี่ยน base dropdown เป็น `uat` ก่อน** create
- 📎 **กฎ: ทุกครั้งที่งานถึงขั้นต้องเปิด PR → ต้องส่งลิงก์เปิด PR (ฟอร์แมตข้างบน) ให้ user เสมอ** — ห้ามจบงานแค่ "push แล้ว" โดยไม่แปะลิงก์ · user ต้องแค่กดลิงก์แล้ว Create ได้เลย

### 2) 🤝 ใครทำขั้นไหน — สำคัญ
| ขั้น | ใครทำ | skill ช่วยได้ไหม |
|---|---|---|
| `feature/* → uat` | **Claude ช่วยได้** (ตามมาตรฐานนี้) | ✅ commit/push/เปิด PR/แนะนำ merge เข้า uat ได้ |
| `uat → main` (ขึ้น production) | **user เท่านั้น** | ❌ **Claude ห้ามเปิด/กด merge PR เข้า main เอง** |

- ขั้น **`uat → main` คือ gate เผยแพร่ขึ้น prod — เป็นการตัดสินใจของคน** Claude ทำได้แค่ **เตรียมให้** (สรุปว่าพร้อมไหม, บอกลิงก์เปิด PR, บอกว่าต้องเช็กอะไร) แล้ว **ส่งให้ user กดเอง**
- ถ้า user สั่งให้ Claude merge `uat → main` → **ปฏิเสธอย่างสุภาพ** + อธิบายว่าขั้น prod ต้อง user กดเอง แล้วชี้ลิงก์/ขั้นตอนให้แทน

---

## 👁️ กฎ: โปร่งใส + แสดงสถานะให้ user เห็นเสมอ

เป้าหมาย: user ต้อง **เห็นชัดว่ากำลังจะเกิดอะไร** และ **รู้ว่าตัวเองอยู่ state ไหน + ต้องทำอะไรต่อ** — ห้ามรัน git เงียบ ๆ

### 1) ก่อนรันคำสั่ง git ทุกครั้ง → โชว์คำสั่ง + อธิบาย
- แสดง git command ที่จะรันเป็น **code block ชัด ๆ** พร้อมคำอธิบายสั้น ๆ ว่า **คำสั่งนี้ทำอะไร + ส่งผลอะไร**
- คำสั่งที่ **กลับยาก/อันตราย** (`push --force`, `reset --hard`, `rebase`, `branch -D`) → เตือนผลกระทบ + ขอ confirm ก่อนรัน
- ตัวอย่างรูปแบบที่ควรแสดง:
  ```bash
  git checkout -b feature/login   # แตก branch ใหม่จาก branch ปัจจุบัน ไว้พัฒนา (ยังไม่กระทบใคร)
  git add src/auth.ts               # เลือกไฟล์เข้า staging เตรียม commit
  git commit -m "feat(auth): ..."   # บันทึกลง history ของ branch นี้ (ยังอยู่แค่ในเครื่อง)
  ```

### 2) ตอบสถานะได้เสมอเมื่อ user ถาม ("ตอนนี้อยู่ตรงไหน / ต้องทำอะไรต่อ")
- เช็กจริงด้วย `git status` · `git branch` · `git log --oneline --graph --all` ก่อนตอบ (อย่าเดา)
- สรุปเป็นภาษาคน + **วาด flow/graph** ให้เห็นว่าอยู่ state ไหน แล้ว **บอกขั้นถัดไป**

  ```
  main ── c1 ── c2 ── c3                      ← main/uat อยู่ที่นี่
                       └── feature/fullstack ── c4   ◄ คุณอยู่ตรงนี้ (ยังไม่ push)

  ขั้นถัดไป:  รัน validate → git push → เปิด PR เข้า uat
  ```
- เน้นชี้ **"ขั้นถัดไปต้องทำอะไร"** เสมอ เพื่อให้ user เดินต่อเองได้

> หลักคิด: git ทำให้ user กลัวเพราะมองไม่เห็น "ตอนนี้อยู่ไหน" — skill นี้มีหน้าที่ทำให้มัน **มองเห็นได้ตลอด**

---

## 🔄 กฎ: เตือนให้ sync เมื่อ feature branch ตามหลัง `uat`

เมื่อทำงาน git บน feature branch (โดยเฉพาะ **ก่อน push / ก่อนเปิด PR / เมื่อ user กลับมาทำ branch เก่า**) ให้เช็กก่อนว่า branch ตามหลัง `uat` แค่ไหน:

```bash
git fetch origin
git rev-list --count HEAD..origin/uat   # uat มีงานใหม่กี่ commit ที่ branch เรายังไม่มี (= ตามหลังเท่านี้)
```

- ถ้าผล **> 0 (ตามหลัง)** → **แจ้งเตือน user เชิงรุก** ว่า _"branch นี้ตามหลัง `uat` อยู่ N commit — ควร sync ก่อนทำต่อ/ก่อนเปิด PR"_ พร้อมเสนอคำสั่ง:
  ```bash
  git merge origin/uat        # (หรือ git rebase origin/uat) นำงานล่าสุดของ uat มารวม
  ```
- **ยิ่ง branch แตกมานาน / ตามหลังเยอะ ยิ่งเน้นเตือน** — branch ที่ทิ้งไว้นานแล้วไม่ sync เสี่ยง conflict ก้อนใหญ่ + เทสบนของเก่า อย่าปล่อยให้ push/PR ทั้งที่ตามหลัง
- เป็นการเตือนเชิงรุก ไม่ต้องรอ user ถาม

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

## 📄 กฎ README.md ต้องมีเสมอ (Mandatory README)

**ทุก project ที่ใช้ git ต้องมีไฟล์ `README.md` เสมอ** และต้องอัปเดตให้ทันสมัย
เมื่อทำงาน git ในโปรเจกต์ใด ๆ (init / commit / push) → ถ้ายังไม่มี README.md หรือมีแต่ไม่ครบ ให้สร้าง/เติมก่อน

`README.md` ต้องมี **2 ส่วนหลัก** ตามลำดับ:

1. **คำอธิบาย project (Project Description)** — โปรเจกต์นี้คืออะไร ทำอะไร แก้ปัญหาอะไร ฟีเจอร์หลัก วิธีเริ่มใช้งาน
2. **Technical Information (ข้อมูลทางเทคนิค)** — ต่อท้ายเสมอ อธิบาย**ทุกอย่างที่ dev ควรรู้**เพื่อทำงานกับโปรเจกต์นี้ได้ เช่น:
   - Tech stack & dependencies (ภาษา/เฟรมเวิร์ก/เวอร์ชัน)
   - โครงสร้างโปรเจกต์ (project structure) — โฟลเดอร์/ไฟล์สำคัญทำหน้าที่อะไร
   - การติดตั้ง & รัน (setup / build / run / test commands)
   - Environment variables & config (รวมถึงไฟล์ `.env.example`)
   - Database / external services / integrations (schema, migration, การเชื่อมต่อ)
   - Architecture / data flow (ภาพรวมการทำงาน, decision สำคัญ)
   - Deployment (deploy ยังไง, environment ไหน) — อ้าง branch model: `main`=prod, `uat`=UAT
   - Conventions & gotchas (ข้อตกลงในทีม, จุดที่พลาดบ่อย, สิ่งที่ต้องระวัง)

> ใช้ `templates/README.template.md` เป็นโครงเริ่มต้นได้เลย — เติมเนื้อหาให้ครบทั้ง 2 ส่วน
> เป้าหมาย: dev คนใหม่เปิด README แล้วเข้าใจและเริ่มงานต่อได้ทันทีโดยไม่ต้องถามใคร

---

## 🚦 Push Rules (สรุป)

1. ❌ ห้าม push ตรงเข้า `main` (บังคับ) — ผ่าน PR เสมอ
2. 🚧 ❌ ห้าม PR ข้าม UAT — `feature/*` PR เข้า `uat` เท่านั้น (base ต้องเป็น `uat` ไม่ใช่ `main`)
3. 🤝 `uat → main` = **user กดเอง** · Claude ช่วยได้แค่ `feature/* → uat`
4. ✅ push เฉพาะ `feature/*` ของตัวเอง
5. ⚠️ force ได้เฉพาะ branch ตัวเอง และใช้ `--force-with-lease`
6. 🔄 pull/rebase ก่อน push เสมอ
7. 🧪 รัน test/lint ก่อน push
8. 🚨 credential gate ต้องผ่าน (ดูด้านบน)
9. 📎 ต้องเปิด PR เมื่อไร → **ส่งลิงก์เปิด PR ให้ user เสมอ** (compare link ฝัง base=uat + title + description — ดูกฎลิงก์ด้านบน)

---

## 🧹 Cleanup หลัง merge (กฎ)

- PR ถูก merge แล้ว → **ลบ feature branch ทั้ง remote และ local**
  - remote: เปิด GitHub **Settings → Automatically delete head branches** (ลบให้อัตโนมัติ) หรือ `git push origin --delete feature/<name>`
  - **local (ต้องลบเองเสมอ):** `git fetch --prune` แล้ว `git branch -d feature/<name>` (`-d` ลบเฉพาะที่ merge แล้ว = ปลอดภัย)
- **ห้ามใช้ feature branch เดิมต่อหลัง merge** — ถ้าต้องแก้เพิ่มทีหลัง ให้ **แตก branch ใหม่จาก `uat` ล่าสุด** เสมอ → ทำงาน → merge เข้า `uat` อีกรอบ
  > 1 รอบงาน = 1 branch อายุสั้น · กัน branch เก่าตามหลัง uat แล้วเกิด conflict/ของซ้อน

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
| `README.template.md` | โครง README (project description + Technical Information) — กฎต้องมีเสมอ |
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
