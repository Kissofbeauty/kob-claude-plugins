# UAT Template + Defect Report Format

> ใช้เป็นแม่แบบเอกสาร UAT (User Acceptance Test) ที่ **อ้าง requirement จาก PM ทุกข้อ**
> copy ไปเก็บที่ repo (เช่น `docs/uat/uat-<feature>.md`) แล้วเติมค่าจริง

---

## 1. ส่วนหัวเอกสาร

```
โปรเจกต์ / Feature : ____________________
เวอร์ชัน / commit  : ____________________
ผู้ทดสอบ (qa)      : ____________________
วันที่ทดสอบ        : ____________________
แหล่ง requirement  : requirements.md / project-proposal.md (อ้าง section/REQ-id)
สภาพแวดล้อมทดสอบ   : (local / uat / staging) + ข้อมูลทดสอบที่ใช้
```

---

## 2. Traceability — requirement ↔ test (ต้องครบทุกข้อ)

> เช็คว่า **ทุก requirement มี test** — ถ้ามีช่องว่าง = ยังทดสอบไม่ครบ

| REQ-id | requirement / acceptance criteria | test case (TC-id) | ประเภท | สถานะ |
|---|---|---|---|---|
| REQ-01 | ผู้ใช้ login ด้วย email/password | TC-01, TC-02, TC-03 | unit + e2e | ✅ |
| REQ-02 | ... | TC-04 | integration | ⏳ |

---

## 3. ตารางผลทดสอบหลัก

| TC-id | REQ-id | ประเภท test | ผลคาดหวัง (Expected) | ผลจริง (Actual) | Pass/Fail | หมายเหตุ / defect-id |
|---|---|---|---|---|---|---|
| TC-01 | REQ-01 | positive | login ถูก → เข้าหน้า dashboard | ตามคาด | ✅ Pass | — |
| TC-02 | REQ-01 | negative | password ผิด → แจ้ง error ไม่ระบุว่า field ไหนผิด | แจ้ง "email/password ไม่ถูกต้อง" | ✅ Pass | — |
| TC-03 | REQ-01 | boundary | password ยาว max+1 → ปฏิเสธ | crash 500 | ❌ Fail | DEF-01 |
| TC-04 | REQ-02 | edge | ส่ง payload ว่าง → 400 | ตามคาด | ✅ Pass | — |
| TC-05 | REQ-01 | security/abuse | SQL injection ใน email → ปฏิเสธ ไม่หลุด query | ตามคาด (parameterized) | ✅ Pass | ผ่าน /skill-cybersecurity-api |

> ประเภท test: positive / negative / edge / boundary / security-abuse

---

## 4. Security checklist (ส่วนหนึ่งของ UAT)

| รายการ | เครื่องมือ | ผล |
|---|---|---|
| code/endpoint vulnerability | `/skill-cybersecurity` หรือ `-api` | ✅ / ❌ / N/A |
| secret/credential leak | `/skill-cybersecurity-secret-scan` | ✅ / ❌ |
| container / IaC (ถ้ามี) | `/skill-cybersecurity-container-iac` | ✅ / ❌ / N/A |
| abuse case ใน test set | (ในตารางข้อ 3) | ✅ / ❌ |

> ถ้า environment ไม่มี security plugin → ระบุไว้ + แจ้ง PM ว่าควรเสริม security review

---

## 5. สรุปผล UAT

```
ทดสอบทั้งหมด : __ test cases
Pass         : __    Fail : __    Blocked : __
requirement ครอบ : __/__ ข้อ
Defect คงค้าง : Critical __ · High __ · Medium __ · Low __
```

**สถานะส่งมอบ:**
- [ ] ✅ ผ่าน UAT — qa อนุมัติส่งมอบ
- [ ] ⚠️ ผ่านแบบมีเงื่อนไข — known issue ที่ PM ยอมรับ (ระบุ): ______
- [ ] ❌ ไม่ผ่าน — มี blocker ต้องเข้า fix loop

> ผู้ตัดสินผ่าน/ไม่ผ่าน = **qa** · เงื่อนไข/known issue = ตัดสินร่วมกับ **PM**

---

## 6. รูปแบบ Defect Report

ทุก Fail ในตารางต้องมี defect report 1 ใบ:

```
[DEF-01] login crash เมื่อ password ยาวเกิน max
─────────────────────────────────────────────
requirement/test ที่กระทบ : REQ-01 / TC-03
severity                  : High   (Critical / High / Medium / Low)
คาดหวัง (Expected)        : ปฏิเสธ input อย่างสุภาพ → HTTP 400 + ข้อความ validation
เกิดจริง (Actual)         : HTTP 500 + stack trace หลุดออก response
ขั้นตอนทำซ้ำ (Steps)      :
  1. ไปหน้า /login
  2. กรอก password 4097 ตัวอักษร
  3. กด submit
หลักฐาน                   : log/response snippet, screenshot
สถานะ                     : Open → In Fix (fullstack) → Retest (qa) → Closed
ผู้แก้ที่มอบหมาย          : subagent-fullstack
หมายเหตุ PM               : (PM ตัดสินว่าแก้ตาม spec / ปรับ requirement / accept)
```

### เกณฑ์ Severity
| ระดับ | ความหมาย |
|---|---|
| **Critical** | ระบบใช้ไม่ได้ / data loss / ช่องโหว่ security ร้ายแรง → ต้องแก้ก่อนส่งมอบ |
| **High** | feature หลักพัง / security ปานกลาง → ควรแก้ก่อนส่งมอบ |
| **Medium** | feature รองพัง มี workaround |
| **Low** | คอสเมติก / ไม่กระทบการใช้งานหลัก |

### Fix loop (ย้ำ)
```
qa report ► fullstack แก้ ► PM ร่วมประเมิน(แก้ตามไหม) ► qa retest+regression
   ▲                                                              │
   └──────────────── ยังไม่ผ่าน วน loop ◄──────────────────────────┘
                     ผ่านทั้งหมด ► qa ปิด UAT
```
