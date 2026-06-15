# skill-backend

## Overview
มาตรฐานการเขียนฝั่ง server / ออกแบบ API ให้ subagent-fullstack เขียน backend ได้คุณภาพดีและปลอดภัย — ครอบ REST/GraphQL design, server patterns (Next.js API routes / Node), validation, auth, error handling และการแยกชั้น controller/service/repository · เชื่อมกับ skill-sql (data), skill-fastapi (Python backend), skill-cybersecurity-api (security)

## วิธีการคิดและการทำงานของ Skill
1. **API design** — REST/GraphQL contract, status codes, pagination, error shape เดียวกันทั้งระบบ
2. **Server patterns** — validate ที่ boundary, error handling รวมศูนย์, ไม่ leak internal
3. **Layering** — controller บาง → service (business logic) → repository (data); business rule ไม่ชัด → ถาม PM
4. **Security** — managed auth, authorization ทุก endpoint, secret จาก env, ตรวจด้วย cybersecurity-api ก่อนส่ง

## ผลลัพธ์ที่ได้จากการใช้งาน
- API/server code ที่ validate ครบ, error สม่ำเสมอ, แยกชั้นชัด
- ลดช่องโหว่ฝั่ง backend (BOLA, broken authz, secret leak)
- backend ที่ส่งต่อ qa-tester แล้วผ่านง่ายขึ้น

## วิธีใช้
```
/skill-backend
/skill-backend            # เมื่อออกแบบ/เขียน API หรือ server-side logic
```

## ตัวอย่าง
```
user: "ทำ API สร้าง order"
→ skill วาง: REST contract + validation schema + controller→service→repository
  + authorization (ผูก owner) + error shape มาตรฐาน + ชี้ตรวจ /skill-cybersecurity-api
```
