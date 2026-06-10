# STRIDE Reference — นิยาม · คำถาม · ตัวอย่าง · control + trust boundary + เทมเพลต

อ้างอิงสำหรับ `skill-cybersecurity-threat-model` — ใช้ตอนทำ Phase 2 (trust boundary), Phase 3 (STRIDE), Phase 6 (เทมเพลต doc)

---

## 1. STRIDE — 6 หมวดภัยคุกคาม

STRIDE จับคู่ภัยคุกคามกับคุณสมบัติความปลอดภัยที่ถูกละเมิด ไล่ทุกหมวดต่อ **แต่ละ element** (process / data store / data flow / external entity) โดยเฉพาะจุดที่ **ข้าม trust boundary**

### S — Spoofing (ปลอมตัว) ↔ ละเมิด Authentication
- **นิยาม:** ผู้โจมตีปลอมเป็น user/service/component อื่นเพื่อเข้าถึงสิ่งที่ไม่ควรได้
- **คำถามชวนคิด:** identity ถูกพิสูจน์ที่จุดไหนบ้าง? service-to-service มี auth ไหม? token/session ปลอม/ขโมยได้ไหม? มี anonymous access ที่ควรต้อง login ไหม?
- **ตัวอย่าง threat:** attacker ใช้ session token ที่รั่วเข้าถึง account คนอื่น · service ภายในเรียก API กันได้โดยไม่ต้อง auth
- **Control ที่ใช้บ่อย:** strong auth (MFA), session management ที่ปลอดภัย, mutual TLS ระหว่าง service, signed token (JWT ที่ verify signature), API key/OAuth2

### T — Tampering (ดัดแปลง) ↔ ละเมิด Integrity
- **นิยาม:** แก้ไขข้อมูลหรือโค้ดโดยไม่ได้รับอนุญาต — ทั้ง in-transit และ at-rest
- **คำถามชวนคิด:** ข้อมูลถูกแก้ระหว่างทางได้ไหม? client ส่งค่าที่ server เชื่อโดยไม่ตรวจ (เช่น price, role)? config/dependency ถูกสับเปลี่ยนได้ไหม?
- **ตัวอย่าง threat:** แก้ราคาใน request ก่อนส่งถึง server · MITM แก้ payload เพราะไม่ได้ใช้ TLS · poison dependency ใน build
- **Control ที่ใช้บ่อย:** TLS ทุก hop, server-side validation/authorization (อย่าเชื่อ client), integrity check (HMAC/digital signature), hashing, immutable audit, signed artifact + SRI

### R — Repudiation (ปฏิเสธความรับผิด) ↔ ละเมิด Non-repudiation
- **นิยาม:** ผู้กระทำปฏิเสธว่าไม่ได้ทำ และระบบพิสูจน์ไม่ได้ เพราะไม่มีหลักฐาน
- **คำถามชวนคิด:** action สำคัญ (โอนเงิน, ลบข้อมูล, เปลี่ยนสิทธิ์) ถูก log ไหม? log แก้/ลบได้ไหม? log ผูกกับ identity จริงไหม?
- **ตัวอย่าง threat:** user ปฏิเสธว่าไม่ได้สั่งทำรายการ เพราะไม่มี audit trail · admin ลบ log ปิดร่องรอย
- **Control ที่ใช้บ่อย:** audit logging ที่ tamper-evident (append-only/WORM), log ผูก timestamp + user id, centralized log, digital signature บน transaction

### I — Information Disclosure (ข้อมูลรั่ว) ↔ ละเมิด Confidentiality
- **นิยาม:** ข้อมูลถูกเปิดเผยต่อผู้ที่ไม่ควรเห็น
- **คำถามชวนคิด:** PII/secret เก็บ/ส่งแบบ plaintext ไหม? error message/response รั่ว detail เกินไปไหม? log มี sensitive data ไหม? object/IDOR เข้าถึง data คนอื่นได้ไหม?
- **ตัวอย่าง threat:** ดึงข้อมูลคนอื่นผ่าน enumerable id (IDOR) · secret โผล่ใน error stack trace/log · backup ไม่ได้เข้ารหัส
- **Control ที่ใช้บ่อย:** encryption at-rest & in-transit, least privilege / per-resource authorization, data minimization, mask PII ใน log, generic error message, secret manager

### D — Denial of Service (ทำให้ใช้ไม่ได้) ↔ ละเมิด Availability
- **นิยาม:** ทำให้ระบบหรือ service ใช้งานไม่ได้สำหรับผู้ใช้ที่ถูกต้อง
- **คำถามชวนคิด:** endpoint ไหน expensive และเรียกรัว ๆ ได้? มี input ที่ทำให้ใช้ resource เกินควร (zip bomb, regex DoS, unbounded query)? single point of failure อยู่ที่ไหน?
- **ตัวอย่าง threat:** flood login endpoint จน DB ล่ม · อัป file ใหญ่ไม่จำกัดจน disk เต็ม · query ไม่มี pagination
- **Control ที่ใช้บ่อย:** rate limiting / throttling, input size limit, timeout + circuit breaker, auto-scaling, quota, CDN/WAF, graceful degradation

### E — Elevation of Privilege (ยกระดับสิทธิ์) ↔ ละเมิด Authorization
- **นิยาม:** ได้สิทธิ์เกินกว่าที่ควร — ทั้ง vertical (user→admin) และ horizontal (user→user อื่น)
- **คำถามชวนคิด:** authz check อยู่ทุก sensitive action ไหม? มี privilege เปลี่ยนข้าม trust boundary ไหม? trust client-side role ไหม? default permission เปิดกว้างไป?
- **ตัวอย่าง threat:** เรียก admin endpoint ตรง ๆ โดยไม่ผ่าน UI gate · แก้ role ใน token แล้ว server ไม่ตรวจ · path traversal เข้าถึงไฟล์ระบบ
- **Control ที่ใช้บ่อย:** server-side RBAC/ABAC ทุก action, deny-by-default, principle of least privilege, validate ทุก trust boundary crossing, sandbox/isolation

---

## 2. วิธีระบุ Trust Boundary

**Trust boundary** = เส้นที่ระดับความเชื่อใจของข้อมูล/ผู้เรียกเปลี่ยนไป — เป็นจุดที่ภัยคุกคามรวมตัวมากสุด ต้องวิเคราะห์ STRIDE เข้มเป็นพิเศษ

มองหาจุดเหล่านี้:
- **Internet ↔ application** (public endpoint, user input ที่ "untrusted" เสมอ)
- **App ↔ data store** (DB, cache, file storage)
- **Service ↔ service** ภายใน (โดยเฉพาะข้าม network/team/VPC)
- **App ↔ 3rd-party / external** (payment, email, OAuth provider, webhook)
- **ระดับสิทธิ์ที่ต่างกัน** (anonymous ↔ user ↔ admin · tenant A ↔ tenant B)
- **Process ↔ OS / runtime** (file system, env, subprocess)

> กฎ: ทุก data flow ที่ **ข้าม** boundary = ต้องถามครบ STRIDE · input จากนอก boundary = untrusted จนกว่าจะ validate

ตัวอย่าง DFD พร้อม boundary (ใช้ `┊` แทนเส้น boundary):

```
                    trust boundary
                          ┊
 [Browser/User] --HTTPS--> ┊ --> [API Gateway] --authz--> [Order Service] --> [(Orders DB)]
   (untrusted)            ┊                                      |
                          ┊                                      +--> [Payment API] (external)
 [Admin] -----HTTPS------> ┊ --> [Admin Console] --RBAC--------> [Order Service]
```

---

## 3. เทมเพลต Threat Model Document

```markdown
# Threat Model — <ชื่อระบบ/feature>
วันที่: <date> · ผู้ทำ: <ชื่อ> · เวอร์ชัน design: <ref>

## 1. Scope & Assets
- ระบบทำอะไร: ...
- In scope: ... · Out of scope: ...
- Assets (เรียงตาม value):
  | Asset | ประเภท | ความสำคัญ |
  |---|---|---|
  | user PII | data/confidential | High |
- Actors: <legit user> / <admin> / <external system> / <attacker + แรงจูงใจ>

## 2. Architecture & Data Flow
- คำอธิบาย component + data flow
- DFD (ASCII) + trust boundaries:
  <แทรก DFD>

## 3. Threats (STRIDE)
| ID | Element / Flow | STRIDE | Threat (actor→action→impact) | Likelihood | Impact | Risk |
|---|---|---|---|---|---|---|
| T-01 | login endpoint | S | attacker ใช้ token ที่รั่ว → เข้า account คนอื่น | Medium | High | High |
| T-02 | order API | E | user เรียก admin endpoint ตรง → แก้ออเดอร์คนอื่น | Medium | High | High |

## 4. Mitigations
| Threat | Control | กลยุทธ์ | Residual Risk |
|---|---|---|---|
| T-01 | short-lived token + MFA + bind to device | Mitigate | Low — เหลือ social-engineering |
| T-02 | server-side RBAC per resource, deny-by-default | Mitigate | Low |

## 5. Residual Risk & Decision
- ความเสี่ยงที่ยังเหลือหลังใส่ control + ต้องให้ใครตัดสินใจรับ/แก้
- Next step (เช่น: ส่งต่อให้ skill-cybersecurity-general ตอนมีโค้ด, pen test, review รอบหน้า)
```

---

## หมายเหตุ
- skill นี้ทำงานระดับ **design** — เมื่อมีโค้ดจริงให้ใช้ `skill-cybersecurity-general` (OWASP) สแกนต่อ เพื่อ verify ว่า control ที่ออกแบบไว้ถูก implement จริง
