# requirements.md — kob-claude-plugins

- **เวอร์ชัน:** 0.1 (draft)
- **เจ้าของ:** ทีม BI · database@kissofbeauty.co.th
- **สถานะ:** เก็บ requirement รอบรากฐาน (foundation + contribution workflow)

---

## 1. วิสัยทัศน์ (WHAT)
สร้าง **plugin marketplace ขององค์กร** ให้ทีม BI (dev หลายคน) ช่วยกันสร้าง/ดูแล
skill · subagent · (ภายหลัง) MCP และให้คนในองค์กร — ทั้งผู้ใช้ **Claude Team** และ
**personal** — ติดตั้งใช้งานได้ **ครั้งเดียวแล้วได้อัปเดตต่อเนื่อง** ผ่านหลาย surface
(Claude Code / chat / cowork) ตามสะดวก

## 2. ผู้เกี่ยวข้อง
- **Maintainer:** ทีม BI dev หลายคน (เพิ่ม/แก้ plugin เรื่อย ๆ)
- **Consumer:** พนักงานในองค์กร — บัญชี Claude Team และ personal
- **Admin:** ผู้ดูแล GitHub org + (ถ้ามี) admin ของ Claude for Work workspace

## 3. Scope รอบนี้ (foundation)
**In scope**
1. โครงสร้าง marketplace + มาตรฐานการจัดวาง plugin/skill/subagent
2. **Contribution workflow** สำหรับ dev หลายคน (branch model, review, versioning, validation)
3. **Distribution strategy** ครอบ 2 surface (Claude Code + claude.ai) + เรื่อง access ของ repo private
4. เอกสารรากฐาน: `CLAUDE.md`, `requirements.md`, `CONTRIBUTING.md`, `README.md` (revise)

**Out of scope (รอบนี้)**
- การบันเดิล **MCP servers** เข้า plugin (เลื่อนไปรอบถัดไป)
- การเขียนเนื้อหา skill ใหม่ (นอกเหนือ `skill-git-standard` ที่มีอยู่)
- ระบบ CI/CD อัตโนมัติเต็มรูปแบบ (วางสเปกไว้ก่อน — implement ทีหลัง)

## 4. การตัดสินใจที่เคาะแล้ว
| # | ประเด็น | มติ |
|---|---|---|
| D1 | เป้าหมายรอบนี้ | วางรากฐาน marketplace + contribution workflow |
| D2 | Surface | Claude Code **และ** claude.ai (chat/cowork) ตั้งแต่แรก |
| D3 | Repo hosting | GitHub org — **private** |
| D4 | MCP | ยังไม่รวมรอบนี้ — เน้น skill/subagent ก่อน |
| D5 | claude.ai publish | องค์กรใช้ **Claude for Team** + ผู้ถาม **เป็น admin** → admin อัป/จัดการ Skills เข้า workspace ให้สมาชิกทั้ง org ได้ |
| D6 | Repo access | GitHub ระดับ **organization** → เพิ่มคนในองค์กรเข้า repo ได้ตรง (org member) |
| D7 | Governance gate | merge เข้า `main` ต้องผ่าน **PR review โดยคน (≥1)** + **security gate** (สแกน secret/ตรวจ skill) |
| D8 | Publish automation | **ปัจจุบันทำได้แค่ manual** ผ่าน admin UI (`claude.ai/admin-settings/skills`) — ยังไม่มี Admin API ให้ automate (Spike S1 ยืนยัน) → คง automate เป็นเป้าหมายอนาคตเมื่อ API เปิด |
| D9 | Branch protection | **ทั้ง `uat` และ `main` protected เหมือนกัน** — บังคับ PR + review ≥1 + CI `validate` + branch up to date + block force push + restrict deletions; **Bypass = `kiss-bim` (admin) คนเดียว** ไว้ break-glass ฉุกเฉินเท่านั้น *(แก้จากเดิมที่ uat เคยหลวม — 2026-06-09)* |

## 5. ข้อเท็จจริง/ข้อจำกัดเชิงเทคนิค (ต้องออกแบบรอบ)
- **F1 — สอง surface คนละกลไกเผยแพร่:**
  - Claude Code: ดึงจาก git repo ตรง ๆ → auto-update เมื่อ `marketplace update`
  - claude.ai (chat/cowork/Projects): **ไม่** pull จาก GitHub → ต้องมีขั้น *publish*
    (admin อัป Skills เข้า workspace หรือใช้ Skills API/console)
- **F2 — repo private + ผู้ใช้ personal:** บัญชีนอก GitHub org จะ `add marketplace`
  ไม่ได้ จนกว่าจะได้สิทธิ์เข้า repo → **แก้ด้วย D6** (เพิ่มเป็น org member + git auth)
  หมายเหตุ: Claude Code ไม่สนว่าบัญชี Claude เป็น Team หรือ personal — ขอแค่ git auth เข้า repo ได้
- **F3 — open format ร่วม:** `SKILL.md` ใช้ได้ทั้งสอง surface → ออกแบบ skill ให้
  **surface-neutral** (ไม่ผูกกับ path/เครื่องมือเฉพาะ Claude Code) เพื่อ reuse ได้
- **F4 — personal บน claude.ai:** Skills ที่ admin push เข้า workspace ได้เฉพาะ **สมาชิกใน Claude for Team workspace** เท่านั้น — ผู้ที่ใช้บัญชี Claude **personal** บน chat/cowork จะไม่ได้รับอัตโนมัติ (ต้องเชิญเข้า workspace หรือ add skill เอง)

## 5.1 Distribution matrix (สรุปช่องทาง)
| ช่องทางใช้งาน | กลไกแจกจ่าย | Auto-update | เงื่อนไขผู้ใช้ |
|---|---|---|---|
| **Claude Code** | `/plugin marketplace add` จาก git repo | ✅ `marketplace update` ดึงจาก git | เป็น org member (สิทธิ์ repo) + git auth |
| **claude.ai chat/cowork/Projects** | admin อัป Skills เข้า Team workspace | ❌ ต้อง re-publish ต่อ release | เป็นสมาชิก Claude for Team workspace |
| (personal บน claude.ai) | ผู้ใช้ add skill เอง | ❌ manual | นอก workspace → เชิญเข้า workspace แนะนำ |

## 6. Acceptance Criteria (รอบรากฐาน)
- [x] AC1 — dev คนใหม่อ่าน `CONTRIBUTING.md` แล้วเพิ่ม skill ใหม่ได้เองโดยไม่ต้องถาม (มีขั้นตอน + ตัวอย่างครบ)
- [x] AC2 — มีมาตรฐานโครงสร้างชัด: ตำแหน่งไฟล์ของ plugin/skill/subagent + วิธีลง entry ใน `marketplace.json`
- [x] AC3 — branch model + review + versioning เขียนชัด สอดคล้องกับ `skill-git-standard`
- [x] AC4 — มีวิธีตรวจ manifest valid ก่อน merge → `scripts/validate.py` + CI `.github/workflows/validate.yml`
- [x] AC5 — distribution strategy ระบุชัด 2 ช่องทาง + ขั้นตอน publish ไป claude.ai + นโยบาย access repo private (§5.1)
- [x] AC6 — `README.md` revise แล้ว: แยกวิธีใช้ 2 surface + ตาราง docs + โครงสร้างใหม่

## 7. Open Questions
- [x] OQ1 — ช่อง publish ไป claude.ai → **ปิดด้วย D5** (Claude for Team, ผู้ถามเป็น admin)
- [x] OQ2 — สิทธิ์เข้า repo private → **ปิดด้วย D6** (org member). คงเหลือประเด็น personal บน claude.ai → ดู F4
- [x] OQ3 — วิธี sync ไป claude.ai → **ปิดด้วย D8** (มุ่ง automate, fallback manual) → เปิด **Spike S1**
- [x] OQ4 — เกณฑ์รับ plugin → **ปิดด้วย D7** (human review + security gate)
- [ ] OQ5 — **ขอบเขต plugin แรก ๆ ที่อยากได้** หลังวางรากฐานเสร็จ (เรียงลำดับความสำคัญ) — รอบถัดไป

## 8. Spikes (งานสำรวจก่อนลงมือ)
- [x] **S1 — Skills management API:** สำรวจแล้ว (มิ.ย. 2026)
  - Claude Team/Enterprise มี **org-wide skill management** ทาง admin UI: อัปครั้งเดียว → provision เปิดให้ทุกคนในองค์กรอัตโนมัติ
  - แจกเฉพาะกลุ่ม: **bundle skills เป็น plugin → assign ให้ group** (plugin ใช้บน claude.ai ได้)
  - **ยังไม่มี Admin API** (`/v1/organizations/` ไม่มี endpoint สำหรับ skills) → CI auto-deploy จาก git **ยังทำไม่ได้** → publish ไป claude.ai = **manual ผ่าน admin UI** จนกว่า API จะเปิด
  - แหล่ง: support.claude.com (provision skills), claude.com/blog (org skills & plugins/groups), github issue #49530 (ขอ Admin API)

## Changelog
- **0.3** — ปิด OQ3/OQ4 ด้วย D7 (human review + security gate) และ D8 (มุ่ง automate publish, fallback manual); เพิ่ม §8 Spike S1 (Skills API)
- **0.2** — ปิด OQ1/OQ2 ด้วยมติ D5 (Claude for Team + admin) และ D6 (GitHub org access); เพิ่ม F4 (personal บน claude.ai) + distribution matrix §5.1
- **0.1** — draft แรก: เก็บวิสัยทัศน์ + scope รากฐาน + 4 มติ (D1–D4) + ข้อจำกัด F1–F3 + AC + open questions
