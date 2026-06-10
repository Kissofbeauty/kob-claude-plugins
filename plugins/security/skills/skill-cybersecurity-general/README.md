# skill-cybersecurity-general

## Overview
Skill สำหรับทำ security vulnerability assessment แบบครอบคลุม **(stack-agnostic — รองรับทุกภาษา/เฟรมเวิร์ก)** เมื่อถูกเรียกใช้จะ detect stack แล้ว scan source code และ configuration files เพื่อหาช่องโหว่ตาม OWASP Top 10:2025 จากนั้นให้คะแนน CVSS เรียงลำดับความเสี่ยง วิเคราะห์ deep dive แต่ละช่องโหว่ และสรุปเป็น security report พร้อม remediation roadmap

## วิธีการคิดและการทำงานของ Skill

1. **Discovery** — สำรวจ target (project ทั้งหมด หรือ path ที่ระบุ) หา source files, configs, dependencies
2. **Scanning** — ตรวจสอบ 10 หมวด OWASP Top 10:2025 ครบทุกหัวข้อ (Injection, Broken Access Control, Crypto Failures ฯลฯ)
3. **Scoring** — ให้คะแนน CVSS v4.0 ประยุกต์ แต่ละช่องโหว่ พิจารณา Exploitability + Impact + Context
4. **Ranking** — เรียงลำดับจาก Critical → High → Medium → Low → Info
5. **Deep Dive** — วิเคราะห์ Root Cause, Attack Scenario, Vulnerable Code, Remediation ทีละช่องโหว่
6. **Report** — สรุป Executive Summary พร้อม Remediation Roadmap

## ผลลัพธ์ที่ได้จากการใช้งาน
- ตารางช่องโหว่เรียงลำดับความเสี่ยงพร้อมคะแนน CVSS
- Deep dive analysis ทุกช่องโหว่ พร้อมโค้ดที่แก้ไขแล้ว
- Executive summary report พร้อม remediation roadmap ระบุ priority

## วิธีใช้
```
/skill-cybersecurity-general
/skill-cybersecurity-general src/auth/client.py
/skill-cybersecurity-general src/
```

## ตัวอย่าง
```
/skill-cybersecurity-general
→ Scans entire project, finds VULN-001 through VULN-N, generates full report

/skill-cybersecurity-general src/auth/login.py
→ Deep scan of single file, focused authentication vulnerability report
```
