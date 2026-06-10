---
name: skill-cybersecurity
description: Cybersecurity expert for screening code/systems for vulnerabilities. Use when user asks to "scan for vulnerabilities", "security review", "check security", "ตรวจสอบช่องโหว่", "security audit", or "/skill-cybersecurity".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-cybersecurity — Security Vulnerability Scanner & Report Generator

เมื่อถูกเรียก ให้ทำ security screening แบบ deep-dive แล้วสรุปเป็น report — **ทำครบทุก Phase ตามลำดับ**

> **Stack-agnostic:** detect ภาษา/เฟรมเวิร์กของ target ก่อน แล้วปรับการ scan ให้เข้ากับ stack นั้น — ไม่ผูกภาษาใดภาษาหนึ่ง

---

## Phase 1: Discovery — สำรวจ target + detect stack

1. ผู้ใช้ระบุ path/ไฟล์/โฟลเดอร์ → scan ตามนั้น · ไม่ระบุ → ทั้ง project ใน working directory
2. **Detect stack ก่อน** จาก manifest แล้วปรับ source glob ตามที่เจอ:

   | Stack | ไฟล์บ่งชี้ | source globs |
   |---|---|---|
   | Python | `pyproject.toml`, `requirements.txt`, `Pipfile` | `*.py` |
   | Node/TS | `package.json` | `*.js`, `*.ts`, `*.jsx`, `*.tsx` |
   | Go | `go.mod` | `*.go` |
   | Java/Kotlin | `pom.xml`, `build.gradle` | `*.java`, `*.kt` |
   | PHP | `composer.json` | `*.php` |
   | Ruby | `Gemfile` | `*.rb` |
   | C#/.NET | `*.csproj`, `*.sln` | `*.cs` |
   | Rust | `Cargo.toml` | `*.rs` |

   > เจอภาษาอื่น/หลายภาษา → หา manifest + นามสกุลหลักของภาษานั้นให้ครบ (ปรับ glob เอง)
3. อ่าน **config + secrets surface** (ทุก stack): `.env*`, `*.config.*`, `*.yaml`/`*.yml`, `*.toml`, `*.ini`, `Dockerfile`, CI config (`.github/`, `.gitlab-ci.yml`)
4. อ่าน **dependency manifest** ที่เจอ (เทียบ version หา known CVE)

---

## Phase 2: Vulnerability Scanning — OWASP Top 10:2025

ตรวจครบทั้ง **A01–A10** ตาม pattern ละเอียดใน **`references/owasp-top10-2025.md`**

> ตัวอย่างใน reference เป็น Python/JS — **pattern ใช้ได้ทุกภาษา** ให้เทียบเคียง equivalent ในภาษาเป้าหมาย (เช่น `os.system` ↔ `exec()` / `Runtime.exec()` / `child_process`)

หมวดที่ต้องครอบ: A01 Access Control · A02 Misconfiguration · A03 Supply Chain · A04 Cryptographic · A05 Injection · A06 Insecure Design · A07 Authentication · A08 Integrity · A09 Logging/Alerting · A10 Exceptional Conditions

---

## Phase 3–6: Score → Rank → Deep-dive → Report

ทำตามเกณฑ์ + เทมเพลตใน **`references/scoring-and-report.md`**:

- **Phase 3 — Risk Scoring:** ให้คะแนนแต่ละช่องโหว่ตาม CVSS v4.0 ประยุกต์ (Critical / High / Medium / Low / Info)
- **Phase 4 — Ranked Finding List:** ตาราง summary เรียงคะแนนสูง→ต่ำ
- **Phase 5 — Deep Dive:** ทุก finding เขียน Root Cause / Attack Scenario / Vulnerable Code / Remediation / Hardening
- **Phase 6 — Executive Summary Report:** สรุปภาพรวม + Critical Actions + Remediation Roadmap

---

## Rules

- ทำครบทุก Phase ห้ามข้าม · ไม่พบในหมวดใดให้ระบุ "✅ No issues found" พร้อมบอกว่าตรวจอะไรไป
- อ้าง **line number จริง**จากไฟล์เสมอ
- remediation ต้องเป็น **working code** ไม่ใช่ pseudo-code
- ให้คะแนนแบบ **อนุรักษ์นิยม**: ไม่แน่ใจระหว่าง High/Medium → เลือก High
- **Defensive เท่านั้น:** ชี้ช่องโหว่ + วิธีแก้/hardening — ไม่เขียน exploit พร้อมใช้

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/owasp-top10-2025.md` | pattern A01–A10 ละเอียด + ตัวอย่างโค้ด |
| `references/scoring-and-report.md` | เกณฑ์ CVSS scoring + เทมเพลต finding/report |
