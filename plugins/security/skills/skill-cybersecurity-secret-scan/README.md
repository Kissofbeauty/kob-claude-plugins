# skill-cybersecurity-secret-scan

## Overview
Skill สำหรับสแกนหา **secret/credential ที่หลุดเข้ามาในโค้ดและ git history** เมื่อถูกเรียกใช้จะสำรวจไฟล์ที่เสี่ยง (source, config, `.env`, notebook, log) แล้วค้นหาตาม pattern ของ secret (cloud key, token, JWT, private key, DB connection string, generic high-entropy) ทั้งใน working tree และ **ทุก commit ของ git history** จากนั้นกรอง false positive จัดชนิด และสรุปเป็น report พร้อม remediation playbook ที่เน้นว่า "ลบไฟล์เฉย ๆ ไม่พอ ต้อง revoke + rotate key"

## วิธีการคิดและการทำงานของ Skill

1. **Discovery** — สำรวจ target (ทั้ง repo หรือ path ที่ระบุ) หาไฟล์ source/config/.env/notebook/log ที่เสี่ยง
2. **Scan working tree** — ค้นหาตาม pattern secret ทุกชนิดในไฟล์ปัจจุบัน
3. **Scan git history** — `git log -p` / `git grep` ทุก commit เพราะ secret ที่ลบไปแล้วยังอยู่ใน history
4. **Classify + verify** — แยกชนิด secret ลด false positive ด้วย context/entropy/placeholder
5. **Report + Remediation** — สรุป finding (mask ค่า) + playbook: revoke/rotate, ล้าง history (BFG/git filter-repo), ย้ายไป secret manager/.env

## ผลลัพธ์ที่ได้จากการใช้งาน
- ตาราง finding ของ secret เรียงตามความร้ายแรง พร้อม `file:line` / commit hash และค่าที่ mask แล้ว
- การจำแนกว่าอยู่ใน working tree หรือ history (พร้อมระดับ confidence)
- Remediation playbook ระบุขั้นตอน revoke + rotate, ล้าง git history, และย้ายไป secret manager

## วิธีใช้
```
/skill-cybersecurity-secret-scan
/skill-cybersecurity-secret-scan src/config/settings.py
/skill-cybersecurity-secret-scan src/
```

## ตัวอย่าง
```
/skill-cybersecurity-secret-scan
→ สแกนทั้ง repo + git history, พบ SECRET-001..N, สร้าง report + remediation playbook

/skill-cybersecurity-secret-scan config/database.yml
→ สแกนไฟล์เดียว เน้น DB connection string / credential ที่ hardcode
```
