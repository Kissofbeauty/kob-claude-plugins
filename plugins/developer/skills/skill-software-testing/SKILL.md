---
name: skill-software-testing
description: Systematic software testing methodology for QA. Use when designing test cases, running unit/integration/e2e tests, doing UAT, writing defect reports, or driving the fix loop. มาตรฐานการทดสอบซอฟต์แวร์อย่างเป็นระบบ — เลือกประเภทการทดสอบ, ออกแบบ test case จาก requirement, security testing, ทำเอกสาร UAT อ้าง requirement จาก PM, และวน defect → fix loop. Trigger on "test software", "ทดสอบซอฟต์แวร์", "เขียน test case", "ทำ UAT", "QA", "write test", "defect report", or "/skill-software-testing".
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# skill-software-testing — Systematic Software Testing & UAT

มาตรฐานการทดสอบของทีม สำหรับ **subagent-qa-tester** — **ยึดตามนี้เสมอ**เมื่อต้องทดสอบงานก่อนส่งมอบ

> หลักการ: **ทุก requirement ต้องมี test ที่พิสูจน์ได้** · ทดสอบต้องคำนึงความปลอดภัย · เจอ defect → วน loop จนผ่าน · **UAT ผูกกับ requirement จาก PM เสมอ**

---

## 1. ประเภทการทดสอบ — เลือกตามบริบท

| ระดับ | ทดสอบอะไร | เลือกเมื่อ |
|---|---|---|
| **Unit** | ฟังก์ชัน/คลาสเดี่ยว แยกอิสระ | มี logic/คำนวณ/branch เยอะ — เร็ว ครอบ edge ได้ลึก |
| **Integration** | หลาย module ต่อกัน (API ↔ DB, service ↔ service) | มี I/O, ต่อ external, contract ระหว่างชิ้น |
| **E2E** | flow ผู้ใช้จริงตั้งแต่ต้นจนจบ (UI/หลาย service) | feature สำคัญ, critical path, regression |
| **UAT** | ผู้ใช้/ตัวแทน user ตรวจว่า "ตรงความต้องการจริงไหม" | ก่อนส่งมอบ — อ้าง requirement จาก PM |

> เริ่มจากระดับล่าง (unit เร็ว+ถูก) ไล่ขึ้นบน · อย่าทดสอบทุกอย่างที่ระดับ e2e (ช้า เปราะ) · **UAT เป็นด่านสุดท้ายเสมอ**

---

## 2. ออกแบบ test case จาก requirement

**กฎ:** map **ทุก requirement / acceptance criteria → test case** (ไม่มี requirement ไหนไม่มี test)

1. อ่าน requirement จาก PM (`docs/features.md` / project-proposal / acceptance criteria) — ใช้ `Read`/`Grep` หา
2. แตกแต่ละ requirement เป็น test case ครอบ 4 มุม:
   - **Positive** — input ถูกต้อง → ได้ผลตามคาด (happy path)
   - **Negative** — input ผิด/ไม่ครบ → error/ปฏิเสธอย่างเหมาะสม (ไม่ crash, ไม่รั่ว)
   - **Edge** — กรณีสุดขอบ: ว่าง, null, ค่าเดียว, ซ้ำ, concurrent, timeout
   - **Boundary** — ค่าขอบเขต: min, max, min-1, max+1 (off-by-one)
3. เขียน test ให้ชัด: **Given / When / Then** + ผลคาดหวังที่วัดได้ (ไม่ใช่ "ควรทำงานถูก")
4. ทำ **traceability** — requirement-id ↔ test-id ไว้เช็คว่า cover ครบ (ดูตารางใน UAT template)

---

## 3. Security testing — ทดสอบต้องคำนึงความปลอดภัย

การทดสอบ functional อย่างเดียวไม่พอ — **ต้องตรวจความปลอดภัยด้วย** โดยเฉพาะงานมี input, auth, หรือ deploy

- ถ้า environment มี plugin **`skill-cybersecurity*`** → เรียกใช้เป็นส่วนหนึ่งของ QA:
  | กรณี | เรียก |
  |---|---|
  | code/endpoint รับ input, auth, business logic | `/skill-cybersecurity` หรือ `/skill-cybersecurity-api` |
  | มี Dockerfile / k8s / IaC | `/skill-cybersecurity-container-iac` |
  | ก่อนส่งมอบทุกครั้ง | `/skill-cybersecurity-secret-scan` (กัน credential หลุด) |
  | full audit ทั้งโปรเจกต์ | `subagent-cybersecurity-auditor` |
- เพิ่ม **abuse case** ใน test set: injection (SQL/cmd/XSS), auth bypass, IDOR, input ใหญ่เกิน, rate limit
- security finding = **defect** → เข้า loop เหมือนบั๊กทั่วไป (ดูข้อ 5) จัด severity ตามผลกระทบ
> ถ้า environment **ไม่มี** security plugin → อย่างน้อยทดสอบ negative/abuse case ด้วยตัวเอง + แจ้ง PM ว่าควรเสริม security review

---

## 4. UAT document — อ้าง requirement จาก PM

ก่อนส่งมอบ ทำ **เอกสาร UAT** ที่ trace กลับ requirement ของ PM ทุกข้อ:

- ตารางหลัก: **req → test → ผลคาดหวัง → ผลจริง → pass/fail → หมายเหตุ**
- สรุปสถานะ: ผ่านกี่ข้อ / fail กี่ข้อ / blocker / ความเสี่ยงค้าง
- เก็บที่ repo (เช่น `docs/uat/` หรือใกล้ requirement) ให้ PM + user ตรวจได้

→ เทมเพลตเต็ม + รูปแบบ defect report: **`references/uat-template.md`**

---

## 5. Defect report → fix loop (สำคัญ)

เจอปัญหา → **เขียน defect report ชัด** อย่ารายงานลอย ๆ:

```
[DEF-xx] หัวข้อสั้น ชัด
- requirement/test ที่กระทบ : REQ-xx / TC-xx
- คาดหวัง (Expected)        : ...
- เกิดจริง (Actual)         : ...
- severity                  : Critical / High / Medium / Low
- ขั้นตอนทำซ้ำ (Steps)      : 1... 2... 3...
- หลักฐาน                   : log / screenshot / response
```

**Loop จนผ่าน:**
```
qa เจอ defect ──► เขียน report ชัด
        │
        ▼
ส่งกลับ subagent-fullstack ให้แก้
        │
        ▼
PM (main agent) ร่วมประเมิน "ควรแก้ตามไหม"   ◄── PM รู้ความต้องการ user สุด
   (อาจปรับ requirement / ลด scope / ยอมรับ known issue)
        │
        ▼
fullstack แก้ ──► qa ทดสอบซ้ำ (regression)
        │
        └──► ยังไม่ผ่าน? วน loop  │  ผ่านทั้งหมด? ► qa ให้ผ่าน ► ปิด UAT
```

> ผู้ตัดสิน "ผ่าน/ไม่ผ่าน" คือ **qa** เท่านั้น · แต่ "แก้ตามไหม/แก้แค่ไหน" ตัดสินร่วมกับ **PM** (เพราะ PM ถือความต้องการ user) · fullstack เป็นผู้แก้

---

## Rules
1. **ทุก requirement/acceptance criteria ต้องมี test** — ไม่มีข้อไหนหลุด (traceability ครบ)
2. ทุก test case ครอบ positive + negative + edge + boundary ตามความเหมาะสม
3. ผลคาดหวัง **วัดได้** เสมอ — ห้าม "ควรทำงานถูก"
4. **security เป็นส่วนหนึ่งของ QA** — เรียก `skill-cybersecurity*` เมื่อมี, secret-scan ก่อนส่งมอบ
5. UAT document ต้อง trace กลับ requirement จาก PM ทุกข้อ
6. defect → report ชัด → fullstack แก้ → PM ร่วมตัดสิน → **วน loop จน qa ให้ผ่าน**
7. ทำ regression หลังแก้ทุกครั้ง — แก้ที่หนึ่ง อย่าพังที่อื่น

## เช็กก่อนปิดงาน
1. requirement ทุกข้อมี test และมีผล (ไม่มี "ยังไม่ทดสอบ")
2. negative/edge/boundary + abuse case ครอบแล้ว
3. security check ผ่าน (skill-cybersecurity* / secret-scan) หรือบันทึกความเสี่ยงที่ค้าง
4. UAT document อัปเดต — สถานะ pass/fail ครบ, defect ที่เหลือมี owner
5. **qa ยืนยันผ่าน** ก่อนส่งมอบ PM

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/uat-template.md` | เทมเพลตเอกสาร UAT เต็ม (traceability + ตารางผลทดสอบ + สรุป) + รูปแบบ defect report |
