---
name: skill-threat-model
description: Proactive design-level threat modeling using STRIDE. Use BEFORE writing code, on an architecture/design/feature description or docs (requirements.md, project-proposal.md) — not a code scan. Trigger when user asks to "threat model", "threat modeling", "STRIDE", "ทำ threat model", "วิเคราะห์ภัยคุกคาม", "ประเมินภัยคุกคามตั้งแต่ออกแบบ", or "/skill-threat-model".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep
---

# skill-threat-model — Design-Level Threat Modeling (STRIDE)

เมื่อถูกเรียก ให้ทำ **threat modeling เชิงรุกระดับ design** — วิเคราะห์ภัยคุกคามจาก **คำอธิบาย architecture / design / feature** หรือ docs (เช่น `requirements.md`, `project-proposal.md`) **ก่อนเขียนโค้ด** — ทำครบทุก Phase ตามลำดับ

> **Input คือ "การออกแบบ" ไม่ใช่ "โค้ด":** skill นี้ไม่สแกนหาช่องโหว่ในโค้ด (ใช้ `skill-cybersecurity` สำหรับงานนั้น) — แต่หาภัยคุกคามที่ติดมากับ **โครงสร้างระบบ** เพื่อแก้ตั้งแต่ยังออกแบบ

## ถ้า input ไม่พอ → ถามก่อน

ถ้าไม่มี design/docs ให้อ่าน ให้ถาม user ก่อนเริ่ม อย่าเดา:
1. **ระบบนี้ทำอะไร** เป้าหมายหลัก + ขอบเขต (in/out of scope)
2. **มี component / service อะไรบ้าง** และคุยกันยังไง (API, queue, DB, 3rd-party)
3. **data / asset สำคัญ** อะไรบ้าง (PII, credential, เงิน, business data)
4. **ใครใช้ / actor** (user, admin, external system, attacker) และ **trust boundary** อยู่ตรงไหน

มี docs ใน repo → ลองอ่าน `requirements.md`, `*proposal*.md`, `README.md`, `docs/` ก่อนถาม

---

## Phase 1: Scope & Assets — ขอบเขต + ของมีค่า

- สรุป **ระบบนี้ทำอะไร** สั้น ๆ + ขอบเขตที่จะ model (in scope / out of scope)
- ระบุ **assets** ที่ต้องปกป้อง: data (PII, credential, secret, เงิน), service availability, ชื่อเสียง
- ระบุ **actors**: ใครใช้บ้าง (legit user, admin, anonymous, external system, **attacker** + แรงจูงใจ)
- จัดลำดับ asset ตาม **value** เพื่อ focus การวิเคราะห์ภายหลัง

## Phase 2: Decompose — ถอดระบบ + วาด trust boundary

- ระบุ **entry points** (ทุกจุดที่ input เข้าระบบ: API endpoint, form, upload, webhook, CLI, queue consumer)
- ระบุ **components / processes / data stores / external entities**
- ลาก **data flow**: ข้อมูลไหลจากไหนไปไหน
- หา **trust boundaries** — เส้นที่ระดับความเชื่อใจเปลี่ยน (internet ↔ app, app ↔ DB, service ↔ 3rd-party, user ↔ admin) → จุดข้าม boundary คือจุดที่ต้องวิเคราะห์เข้ม
- วาด **DFD** แบบ ASCII หรืออธิบายเป็นข้อความ เช่น:

```
[User] --HTTPS--> ┊ [API Gateway] --> [Auth Svc] --> [DB]
 (untrusted)      ┊        |
                  ┊        +--> [3rd-party Payment] (external trust)
        trust boundary ┊
```

> วิธีระบุ trust boundary + ตัวอย่าง DFD แบบละเอียด ดู `references/stride-reference.md`

## Phase 3: STRIDE Analysis — ไล่ทีละ element

สำหรับ **แต่ละ element / data flow / จุดข้าม trust boundary** ไล่ครบ 6 หมวด STRIDE:

| | หมวด | ละเมิดคุณสมบัติ | คำถามหลัก |
|---|---|---|---|
| **S** | Spoofing | Authentication | ปลอมเป็นคนอื่น/ระบบอื่นได้ไหม |
| **T** | Tampering | Integrity | แก้ data/code ระหว่างทางหรือ at-rest ได้ไหม |
| **R** | Repudiation | Non-repudiation | ปฏิเสธว่าไม่ได้ทำได้ไหม (ไม่มี log/audit) |
| **I** | Information Disclosure | Confidentiality | ข้อมูลรั่วถึงคนที่ไม่ควรเห็นได้ไหม |
| **D** | Denial of Service | Availability | ทำให้ระบบล่ม/ใช้ไม่ได้ได้ไหม |
| **E** | Elevation of Privilege | Authorization | ยกระดับสิทธิ์เกินที่ควรได้ไหม |

> นิยาม + คำถามชวนคิด + ตัวอย่าง threat + control ที่ใช้บ่อยของแต่ละหมวด ดู `references/stride-reference.md`
> ให้ตั้ง threat เป็นรูปประโยค "**[actor] สามารถ [ทำอะไร] โดย [วิธี] ส่งผลให้ [ผลกระทบ]**"

## Phase 4: Rank — likelihood × impact

ให้คะแนนแต่ละ threat:
- **Likelihood** (โอกาสเกิด): High / Medium / Low — พิจารณาความง่าย, ต้องมี precondition อะไร, ใครทำได้
- **Impact** (ผลกระทบ): High / Medium / Low — เทียบกับ asset value ใน Phase 1
- **Risk = Likelihood × Impact** → Critical / High / Medium / Low (ไม่แน่ใจ → ปัดขึ้น)

## Phase 5: Mitigations — control ต่อ threat

- เสนอ **control ที่ปฏิบัติได้จริง** ต่อ threat แต่ละตัว (ทำได้ในระดับ design/architecture)
- เลือกกลยุทธ์: **Mitigate** (เพิ่ม control) / **Eliminate** (ตัด feature/flow ทิ้ง) / **Transfer** (ผลักไป 3rd-party/insurance) / **Accept** (รับความเสี่ยง ถ้าต่ำ)
- แยกให้ชัด: threat ที่ **mitigate แล้ว** vs **residual risk** (ความเสี่ยงที่ยังเหลือหลังใส่ control)

## Phase 6: Output — Threat Model Document

ออกเป็นเอกสารตามเทมเพลตใน `references/stride-reference.md` ประกอบด้วย:
- System overview + scope + assets + actors
- DFD + trust boundaries
- **ตาราง threat** (ID · element · STRIDE · threat · likelihood · impact · risk)
- **ตาราง mitigation** (threat → control → กลยุทธ์ → residual risk)
- สรุป residual risk ที่ต้องตัดสินใจรับ/แก้ + ข้อเสนอ next step

---

## Rules

- ทำครบทุก Phase ห้ามข้าม · ไล่ STRIDE ครบ 6 หมวดต่อทุก element ที่สำคัญ · หมวดไหนไม่มี threat ให้ระบุ "ไม่พบ" พร้อมเหตุผล
- input ไม่พอ (ไม่มี design) → **ถาม user ก่อน** อย่าเดา architecture
- **Defensive เท่านั้น:** ชี้ภัยคุกคาม + control/วิธีลดความเสี่ยง — ไม่เขียน exploit หรือ attack tool พร้อมใช้
- mitigation ต้อง **ปฏิบัติได้จริง** ในระดับ design (เช่น "ใช้ mutual TLS", "เพิ่ม authz check ต่อ resource") ไม่ใช่คำลอย ๆ
- แยก **threat ที่ mitigate แล้ว** ออกจาก **residual risk** ให้ชัดเสมอ
- เป็นงาน design — **ไม่อ้าง line number โค้ด** (ถ้ามีโค้ดให้สแกน ใช้ `skill-cybersecurity`)

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/stride-reference.md` | STRIDE 6 หมวด (นิยาม + คำถาม + ตัวอย่าง threat + control) · วิธีระบุ trust boundary · เทมเพลต threat model doc |
