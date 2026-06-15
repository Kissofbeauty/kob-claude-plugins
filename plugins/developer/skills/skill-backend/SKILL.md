---
name: skill-backend
description: Backend / API & server design standard for code quality. Use when designing or writing server-side code — REST/GraphQL APIs, Next.js API routes / Node (Express/Nest) handlers, validation, auth, error handling, or service/repository layering. Trigger on "เขียน backend", "ออกแบบ API", "server", "endpoint", "REST/GraphQL", "Next API route", or "/skill-backend".
allowed-tools: Read, Glob, Grep, Write, Edit
---

# skill-backend — Backend / API & Server Design

มาตรฐานการเขียน **ฝั่ง server** ให้คุณภาพดีและปลอดภัย — ใช้คู่กับ frontend-web (client), sql (data), fastapi/python (Python backend)

> **Defensive + ปลอดภัย:** validate ที่ boundary, ไม่มี secret ในโค้ด, fail closed · เชื่อมโยง `skill-cybersecurity-api` (OWASP API Top 10)

---

## 1. API Design
- **REST:** resource เป็นคำนาม (`/orders/:id`) · ใช้ method/status code ให้ถูก (200/201/204/400/401/403/404/409/422/500) · versioning (`/v1`) · pagination (cursor/keyset) + filtering ที่ชัด
- **GraphQL:** schema-first · resolver บาง · กัน N+1 ด้วย dataloader/batch
- **Contract ชัด:** request/response shape คงเส้นคงวา · **error shape เดียวกันทั้งระบบ** (`{ error: { code, message, details } }`)
- ออกแบบ contract ก่อนเขียน (อิง requirement/proposal จาก PM)

## 2. Server Patterns
- **Next.js:** ใช้ Route Handlers / API routes · แยก logic ออกจาก handler
- **Node (Express/Nest):** middleware เป็นชั้น (auth, validation, error) · ลำดับชัด
- **Validation ที่ boundary:** ตรวจ input ทุก request ด้วย schema (zod / pydantic / class-validator) — อย่าเชื่อ client
- **Error handling รวมศูนย์:** error handler กลาง · ไม่ leak stack trace สู่ client (A02/A10) · log ฝั่ง server (ไม่ log secret/PII)

## 3. Layering (แยกชั้นให้ชัด)
```
HTTP (controller/handler)  →  Service (business logic)  →  Repository (data → skill-sql)
```
- **Controller บาง** — แค่รับ request/validate/เรียก service/ส่ง response
- **Business rule อยู่ใน service** ไม่ใช่ใน controller/SQL
- **Repository** คุยกับ DB อย่างเดียว (parameterized query — ดู `skill-sql`)
- ❗ business rule ไม่ชัด → หยุด ถาม PM (ตามหลัก skill-PM — rule ไหลจาก business → PM)

## 4. Auth & Security
- ใช้ **managed auth** (Supabase/Clerk ตาม architecture-standard) — ❌ ไม่ hand-roll
- verify token/session **ฝั่ง server เสมอ** · authorization check ทุก endpoint ที่ละเอียดอ่อน (กัน BOLA/broken-function-authz — A01/API1/API5)
- secret มาจาก **env/secret manager** ไม่ hardcode · rate limit + idempotency บน endpoint สำคัญ
- ก่อนส่งงาน → ตรวจด้วย **`/skill-cybersecurity-api`** + secret-scan

---

## Rules
- validate input ทุก boundary · error shape เดียว · ไม่ leak internal/stack
- business logic อยู่ service ไม่ใช่ controller/SQL
- ❌ ไม่มี secret ในโค้ด · ❌ ไม่ hand-roll auth/crypto
- authorization ตรวจทุก endpoint ที่เข้าถึงข้อมูลผู้ใช้
- เจอ business rule ไม่ชัด → ถาม PM ไม่เดาเอง

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/backend-patterns.md` | REST/GraphQL · layering · validation · error shape · ตัวอย่าง bad→good |
