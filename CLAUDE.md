# CLAUDE.md — kob-claude-plugins

> บริบทโปรเจกต์สำหรับ Claude (และ dev ทุกคน) อ่านไฟล์นี้ก่อนเริ่มงานเสมอ
> ภาษาในการทำงาน/เขียน docs: **ภาษาไทย** เว้นแต่ผู้ใช้ขออย่างอื่น

## Overview
**kob-claude-plugins** คือ **Claude Code plugin marketplace** ชื่อ `kissofbeauty` ขององค์กร
Kiss of Beauty ดูแลโดยทีม **BI** เป้าหมาย: รวม skill / subagent / (ภายหลัง) MCP
ให้คนในองค์กรติดตั้งครั้งเดียวแล้วใช้ได้ทุก project และได้รับอัปเดตอัตโนมัติ

- **ผู้พัฒนา:** ทีม BI (dev หลายคนช่วยกันเพิ่ม/แก้ plugin)
- **ผู้ใช้:** คนในองค์กร ทั้งที่ใช้ **Claude Team** และ **personal**
- **Surface เป้าหมาย:** Claude Code **และ** claude.ai (chat / cowork / Projects)

## Tech stack
- ไม่มี runtime — เป็น repo ของ **content/manifest** (Markdown + JSON)
- `marketplace.json` / `plugin.json` = manifest ตามสเปก Claude Code plugins
- `SKILL.md` = Agent Skills open format (ใช้ได้ทั้ง Claude Code และ claude.ai)

## Docs map (source of truth)
| ไฟล์ | เก็บอะไร |
|---|---|
| `CLAUDE.md` (ไฟล์นี้) | บริบทโปรเจกต์ + ทางลัดเข้าใจ repo |
| `requirements.md` | requirement + scope + acceptance criteria + open questions/risks |
| `CONTRIBUTING.md` | วิธีที่ dev เพิ่ม/แก้ plugin · branch model · review · versioning |
| `README.md` | หน้าร้าน: วิธีติดตั้ง/อัปเดตสำหรับ teammate |

## Project structure
```
.
├── .claude-plugin/marketplace.json   # สารบัญ marketplace (kissofbeauty)
├── plugins/
│   └── devops/                       # plugin
│       ├── .claude-plugin/plugin.json
│       └── skills/skill-git-standard/  (SKILL.md + references/ hooks/ templates/)
├── CLAUDE.md · requirements.md · CONTRIBUTING.md · README.md
└── .gitignore
```

## Conventions & workflow
- **Branch model (org standard):** `main` (prod/เผยแพร่) ← `uat` ← `feature/<name>`
  - แตก feature จาก `main` → merge เข้า `uat` ทดสอบ → merge เข้า `main`
  - ทั้ง `uat` และ `main` protected เหมือนกัน เข้าได้ผ่าน **PR เท่านั้น** (PR + review + CI · bypass = admin `kiss-bim` ไว้ฉุกเฉิน)
- **Commit:** Conventional Commits (`feat:`/`fix:`/`chore:`/`docs:`…)
- **Credential gate:** pre-commit สแกน secret ก่อน commit (ดู `skill-git-standard`)
- **Versioning:** plugin ไม่ตั้ง `version` → ทุก commit บน `main` = เวอร์ชันล่าสุด (auto-update ฝั่ง Claude Code)
- รายละเอียดทั้งหมด → ใช้ skill **`skill-git-standard`** เป็นมาตรฐานบังคับเมื่อทำงาน git

## Distribution (2 ช่องทาง — สำคัญ)
- **Claude Code:** `/plugin marketplace add <org/repo>` → `/plugin install <plugin>@kissofbeauty` → `update` ดึงจาก git อัตโนมัติ
- **claude.ai (chat/cowork):** ไม่ pull จาก GitHub — ต้อง **publish ซ้ำ** (admin อัป Skills เข้า workspace / Skills API)
- หลักการ: **เขียน skill ครั้งเดียว (surface-neutral SKILL.md) เผยแพร่ 2 ช่องทาง**

## Subagent roster (เมื่อเริ่มพัฒนา — อิง skill-PM)
architect · fullstack · ux-ui · security · devops · qa
(โปรเจกต์นี้เน้น docs/standard เป็นหลัก — เรียก subagent เมื่อมีงาน build/tooling จริง)

## Constraints & gotchas
- repo **private** → ผู้ใช้ต้องมีสิทธิ์เข้า GitHub org ถึงจะ `add marketplace` ได้ (รวมผู้ใช้ personal)
- claude.ai ไม่ auto-update จาก git → ต้องมี publish step (ดู `requirements.md` open questions)
- **secret/PII ห้ามหลุดเข้า git** — `.gitignore` ต้องครอบ `.env`, ไฟล์ลับ
- manifest ต้อง valid เสมอ (marketplace.json / plugin.json) — JSON เสียทำให้ทั้ง marketplace พัง

## Commands
- ติดตั้ง (teammate): ดู `README.md`
- เพิ่ม skill/plugin: ดู `CONTRIBUTING.md`
