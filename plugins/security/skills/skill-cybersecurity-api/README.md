# skill-cybersecurity-api

## Overview
Skill สแกนความปลอดภัยของ API (REST/GraphQL/gRPC) ตาม **OWASP API Security Top 10:2023** — stack-agnostic detect framework แล้วไล่ตรวจ endpoint หาช่องโหว่ (เน้น authorization ที่เป็นปัญหาอันดับต้น ๆ ของ API) สรุปเป็น report จัดระดับความเสี่ยง + วิธีแก้

## วิธีการคิดและการทำงานของ Skill
1. **Discovery** — detect framework + ทำรายการ endpoint/method/auth + เทียบกับ API spec (หา shadow API)
2. **Scan** — ตรวจ API1–API10:2023 (BOLA, Broken Auth, Property-level Authz, Resource Consumption, Function-level Authz, Business Flows, SSRF, Misconfig, Inventory, Unsafe Consumption)
3. **Score & Report** — จัดระดับ + deep-dive ทุก finding + executive summary

## ผลลัพธ์ที่ได้จากการใช้งาน
- ตาราง finding ต่อ endpoint เรียงความเสี่ยง
- วิเคราะห์ + โค้ดแก้ไขต่อช่องโหว่
- สรุปภาพรวม authorization posture ของ API

## วิธีใช้
```
/skill-cybersecurity-api
/skill-cybersecurity-api src/routes/
/skill-cybersecurity-api openapi.yaml
```

## ตัวอย่าง
```
/skill-cybersecurity-api src/api/
→ ไล่ทุก endpoint, จับ BOLA/Broken Function Authz, รายงานพร้อมวิธีแก้
```
