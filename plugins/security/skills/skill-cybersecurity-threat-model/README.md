# skill-cybersecurity-threat-model

## Overview
Skill สำหรับทำ **threat modeling เชิงรุกระดับ design** ด้วยกรอบ **STRIDE** — วิเคราะห์ภัยคุกคามจาก **คำอธิบาย architecture / design / feature** หรือเอกสาร (เช่น `requirements.md`, `project-proposal.md`) **ก่อนเขียนโค้ด** ไม่ใช่การสแกนโค้ด เป้าหมายคือหาภัยคุกคามที่ติดมากับโครงสร้างระบบเพื่อแก้ตั้งแต่ขั้นออกแบบ แล้วสรุปเป็น Threat Model document พร้อม mitigation และ residual risk

> ต่างจาก `skill-cybersecurity-general` ที่สแกนช่องโหว่ในโค้ดตาม OWASP — skill นี้ทำงานก่อนหน้านั้น ที่ระดับ design ถ้ามีโค้ดจริงแล้วให้ใช้ทั้งสอง skill เสริมกัน

## วิธีการคิดและการทำงานของ Skill

1. **Scope & Assets** — ระบบทำอะไร, asset/data สำคัญ, actor/ผู้ใช้คือใคร
2. **Decompose** — entry points, components, data flow, และ **trust boundaries** (วาด DFD)
3. **STRIDE Analysis** — ไล่ทีละ element ครบ 6 หมวด: Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege
4. **Rank** — ให้คะแนน likelihood × impact → ระดับ risk
5. **Mitigations** — เสนอ control ที่ปฏิบัติได้จริงต่อแต่ละ threat
6. **Output** — Threat Model document (ตาราง threat + mitigation + residual risk)

> ถ้า input ไม่พอ (ไม่มี design) skill จะถาม user ก่อน — ระบบทำอะไร, มี component/data/trust boundary อะไร

## ผลลัพธ์ที่ได้จากการใช้งาน
- DFD + trust boundaries ของระบบ
- ตาราง threat ตาม STRIDE พร้อมคะแนน likelihood/impact/risk
- ตาราง mitigation (control + กลยุทธ์ต่อ threat) แยก threat ที่ mitigate แล้ว vs residual risk
- Threat Model document พร้อม next step

## วิธีใช้
```
/skill-cybersecurity-threat-model
/skill-cybersecurity-threat-model requirements.md
/skill-cybersecurity-threat-model "ออกแบบ API ให้ user อัปโหลดไฟล์ แล้วเก็บใน S3 + DB"
```

## ตัวอย่าง
```
/skill-cybersecurity-threat-model project-proposal.md
→ อ่าน design, วาด DFD + trust boundaries, ไล่ STRIDE ทุก element, ออก Threat Model doc

/skill-cybersecurity-threat-model
→ ไม่มี design ให้อ่าน → ถาม user เรื่องระบบ/component/asset/trust boundary ก่อนเริ่ม
```
