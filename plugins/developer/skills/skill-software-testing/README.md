# skill-software-testing

## Overview
skill ความรู้สำหรับ **subagent-qa-tester** ใช้ทดสอบซอฟต์แวร์อย่างเป็นระบบก่อนส่งมอบ — เลือกประเภทการทดสอบ (unit/integration/e2e/UAT) ตามบริบท, ออกแบบ **test case จาก requirement ของ PM ครบทุกข้อ** (positive/negative/edge/boundary), ผนวก **security testing** (เรียก `skill-cybersecurity*` เมื่อ environment มี), ทำ **เอกสาร UAT** ที่ trace กลับ requirement, และขับ **defect → fix loop** จน qa ให้ผ่าน

## วิธีการคิดและการทำงานของ Skill
1. **เลือกระดับการทดสอบ** — unit เร็ว/ลึก → integration → e2e → UAT เป็นด่านสุดท้าย
2. **map requirement → test** — ทุก acceptance criteria มี test, ครอบ positive/negative/edge/boundary, ผลคาดหวังวัดได้
3. **security เป็นส่วนหนึ่งของ QA** — เพิ่ม abuse case + เรียก `/skill-cybersecurity`, `-api`, `-container-iac`, `-secret-scan` เมื่อมี
4. **UAT document** — ตาราง req → test → ผล → pass/fail (เทมเพลตใน references)
5. **defect loop** — qa report ชัด → fullstack แก้ → PM ร่วมตัดสินว่าแก้ตามไหน → วน loop จน **qa ให้ผ่าน**

## ผลลัพธ์ที่ได้จากการใช้งาน
- ชุด test case ที่ trace กลับ requirement ครบทุกข้อ (positive/negative/edge/boundary + abuse case)
- เอกสาร UAT พร้อมสถานะ pass/fail และ traceability
- defect report ที่ชัดเจน + flow การวน fix loop ระหว่าง qa / fullstack / PM
- การทดสอบที่คำนึงถึงความปลอดภัย (ผูกกับ security plugin)

## วิธีใช้
```
/skill-software-testing
/skill-software-testing            # เมื่อจะทดสอบ feature / ทำ UAT / เขียน test case
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อทำงาน QA / test / UAT / defect report

## ตัวอย่าง
```
user: "ทดสอบ feature login ให้หน่อย ก่อนส่งมอบ"
→ skill อ่าน requirement จาก PM, map เป็น test case (positive/negative/edge/boundary),
  เพิ่ม abuse case + เรียก /skill-cybersecurity-api, รันทดสอบ,
  เขียนเอกสาร UAT (req → test → ผล → pass/fail),
  เจอ defect → report ชัด → ส่ง fullstack แก้ → PM ร่วมตัดสิน → วน loop จน qa ผ่าน
```

## ไฟล์ใน skill
| ไฟล์ | เนื้อหา |
|---|---|
| `SKILL.md` | methodology: ประเภทการทดสอบ · ออกแบบ test case · security testing · UAT · defect loop |
| `references/uat-template.md` | เทมเพลต UAT เต็ม (traceability + ผลทดสอบ + สรุป) + รูปแบบ defect report + เกณฑ์ severity |
