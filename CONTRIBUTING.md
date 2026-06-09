# CONTRIBUTING — kob-claude-plugins (kissofbeauty marketplace)

คู่มือสำหรับ **dev ทีม BI** ที่จะเพิ่ม/แก้ plugin · skill · subagent
> มาตรฐาน git ทั้งหมดใช้ skill **`skill-git-standard`** เป็นตัวบังคับ — ส่วนนี้สรุปเฉพาะที่เกี่ยวกับ repo นี้

---

## 0. ก่อนเริ่ม
- ขอสิทธิ์เข้า GitHub org (repo เป็น **private**) + ตั้งค่า git auth (`gh auth login` หรือ SSH key)
- **ตั้ง git identity เป็นของตัวเอง** (commit จะได้ระบุชื่อคนทำถูกต้อง — ทีมใช้ชื่อจริงต่อคน):
  ```bash
  git config user.name  "<ชื่อคุณ>"
  git config user.email "<email ที่ verify ใน GitHub>"
  ```
  > email ต้องถูก **เพิ่ม + verify** ในบัญชี GitHub (Settings → Emails) ไม่งั้น commit จะแสดงชื่อแต่ไม่ลิงก์โปรไฟล์/avatar · อย่าใช้ identity กลาง (เช่น BI-Team) commit แทนกัน
- อ่าน `CLAUDE.md` (บริบทโปรเจกต์) และ `requirements.md` (scope ปัจจุบัน)
- ติดตั้ง marketplace ของตัวเองไว้ทดสอบ: `/plugin marketplace add <org/repo>`

## 1. Branch model (org standard)
```
main (เผยแพร่) ──◄── uat (ทดสอบรวม) ──◄── z-feature/<ชื่องาน>
```
- แตกงานใหม่จาก `main`: `git checkout main && git pull && git checkout -b z-feature/<name>`
- `uat`: **ไม่บังคับ PR** — merge เข้าเพื่อทดสอบได้เลย
- `main`: **protected** เข้าได้ผ่าน **PR เท่านั้น** (PR + review + CI ผ่าน) — bypass มีแค่ admin `kiss-bim` ไว้ break-glass ฉุกเฉิน (ห้ามใช้เป็นทางปกติ)

## 2. โครงสร้างที่ต้องวางให้ถูก
```
plugins/<plugin>/
├── .claude-plugin/plugin.json        # manifest ของ plugin (ห้ามตั้ง "version" — ใช้ auto-update)
├── skills/<skill-name>/SKILL.md       # 1 โฟลเดอร์ = 1 skill
│   ├── references/  templates/  hooks/  (ถ้ามี)
└── agents/<name>.md                   # subagent (ถ้ามี — ใส่ Skill ใน tools ถ้าต้องเรียก skill)
```
ทุก plugin ต้องมี entry ใน `.claude-plugin/marketplace.json`

## 3. เพิ่มของใหม่ — ทำยังไง

### 3.1 เพิ่ม skill ใน plugin เดิม
1. สร้าง `plugins/<plugin>/skills/<skill-name>/SKILL.md`
2. ใส่ frontmatter ให้ครบ:
   ```yaml
   ---
   name: <skill-name>            # kebab-case ตรงกับชื่อโฟลเดอร์
   description: <บอกชัดว่าทำอะไร + เมื่อไรควรถูกเรียก (trigger)>
   ---
   ```
3. เขียนเนื้อหาแบบ **surface-neutral** (ใช้ได้ทั้ง Claude Code และ claude.ai — เลี่ยงผูก path/เครื่องมือเฉพาะ Claude Code)
4. ไฟล์ประกอบใส่ `references/` `templates/` `hooks/`

### 3.2 เพิ่ม plugin ใหม่
1. สร้าง `plugins/<name>/.claude-plugin/plugin.json`
   ```json
   {
     "name": "<name>",
     "description": "<หน้าที่ของ plugin>",
     "author": { "name": "BI-Team", "email": "database@kissofbeauty.co.th" },
     "keywords": ["..."]
   }
   ```
2. เพิ่ม entry ใน `.claude-plugin/marketplace.json` (`name`, `source`, `description`)
3. อัปเดต `README.md` (ตาราง plugin)

### 3.3 เพิ่ม subagent
- สร้าง `plugins/<plugin>/agents/<name>.md` พร้อม frontmatter (name, description, tools)
- ถ้า subagent ต้องเรียก skill → ใส่ `Skill` ใน `tools`

## 4. Validation ก่อนเปิด PR (กัน marketplace พัง)

**รันตัวตรวจอัตโนมัติตัวเดียวครอบคลุม** (ต้องผ่านก่อนเปิด PR — CI รันให้ซ้ำทุก push/PR):
```bash
python scripts/validate.py
```
สคริปต์นี้ตรวจให้ครบ: marketplace.json valid + key ครบ, ทุก entry มี `name`/`source`/`description` และ source path มีจริง, plugin.json ทุกตัว valid + มี `name`/`description`, และ SKILL.md ทุกตัวมี frontmatter ที่ `name` ตรงชื่อโฟลเดอร์ + `description` ไม่ว่าง (exit 0 = ผ่าน, 1 = มี error). ใช้ stdlib ล้วน ไม่ต้องลง lib เพิ่ม

> CI: `.github/workflows/validate.yml` รัน `python scripts/validate.py` อัตโนมัติทุก `push`/`pull_request` — PR ที่ validator ไม่ผ่านจะ merge ไม่ได้

checklist เดิม (ตอนนี้ครอบคลุมโดย `validate.py` ข้อ 1-3 แล้ว — เหลือไว้เป็นแนวคิด):
- [x] JSON ทุกไฟล์ valid (marketplace.json + plugin.json ทุกตัว) — *ตรวจอัตโนมัติ*
- [x] `name` ใน SKILL.md / plugin.json ตรงกับชื่อโฟลเดอร์ — *ตรวจอัตโนมัติ*
- [ ] `description` มี trigger ชัด (ไม่งั้น skill จะไม่ถูกหยิบมาใช้) — *validator เช็กแค่ว่าไม่ว่าง คุณภาพ trigger ยังต้องดูด้วยคน*
- [ ] ทดสอบติดตั้งจาก branch จริง: `/plugin marketplace update` แล้วลองเรียก skill
- [ ] **ไม่มี secret/PII** หลุดเข้า git (pre-commit credential gate ต้องผ่าน)

## 5. Commit & PR
- Conventional Commits: `feat(devops): add docker skill` · `fix:` · `chore:` · `docs:`
- 1 PR = 1 เรื่อง · เขียน description ว่าเพิ่ม/แก้อะไร + วิธีทดสอบ
- ลงท้าย commit ตามมาตรฐานทีม (ดู `skill-git-standard`)

## 6. Governance gate (ก่อน merge เข้า `main`)
ทุก PR เข้า `main` ต้องผ่าน **2 ด่าน** (อิง requirements D7):
1. **Human review ≥1 คน** — reviewer ทีม BI อนุมัติ (1 PR = 1 reviewer เป็นอย่างน้อย)
2. **Security gate** — pre-commit credential scan ผ่าน + ตรวจว่า skill/manifest ไม่มี secret, ไม่ดึงสิ่งอันตราย
> `main` protected: ไม่ผ่าน 2 ด่านนี้ merge ไม่ได้

## 7. Versioning & release
- plugin **ไม่ตั้ง `version`** → ทุก merge เข้า `main` ถือเป็นเวอร์ชันล่าสุด
- ฝั่ง **Claude Code:** ผู้ใช้ได้อัปเดตด้วย `/plugin marketplace update kissofbeauty` (auto จาก git)
- ฝั่ง **claude.ai (chat/cowork):** ต้อง **publish ซ้ำ** เข้า Team workspace
  - **ปัจจุบัน manual เท่านั้น:** admin อัป/อัปเดต skill ที่เปลี่ยนที่ `claude.ai/admin-settings/skills` → provision เปิดให้ทุกคนอัตโนมัติ (แจกเฉพาะกลุ่ม = bundle เป็น plugin แล้ว assign group)
  - **automate (CI) ยังทำไม่ได้** — ยังไม่มี Admin API (requirements Spike S1) เป็นเป้าหมายอนาคต

## 8. Checklist ก่อน merge เข้า main
1. ทดสอบติดตั้ง + เรียกใช้ได้จริง
2. manifest valid · โครงสร้างตามมาตรฐาน
3. docs ที่เกี่ยวข้องอัปเดต (`README.md` / `CLAUDE.md` ถ้ากระทบ)
4. ผ่าน governance gate §6 (review + security)
