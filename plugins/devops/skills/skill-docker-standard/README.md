# skill-docker-standard

## Overview
มาตรฐานการ containerize ของทีม — กำหนดทิศทางว่าแอปที่รันบน server ต้องทำเป็น container ด้วย **docker compose** (dev local) และ **build เป็น image** โดยมี **2 บทบาท**: ทุกคน dev/ทดสอบใน local (ไม่ push image, ไม่มี credential ใน image) ส่วนทีม BI เท่านั้นที่ build official image จาก `main` ผ่าน CI/CD แล้ว push ขึ้น **Docker Hub (private)** + deploy prod

## วิธีการคิดและการทำงานของ Skill
1. **แยกบทบาท** — ทุกคน: compose dev + source ขึ้น GitHub (ไม่ push image) · BI: promote หลัง approve
2. **No credential in image** — secret มาจาก runtime/env_file/CI secret เสมอ (มี checklist + .dockerignore + multi-stage)
3. **Official image จาก main** — CI build จาก source ที่ approve แล้ว ไม่เอา image จากเครื่อง user
4. **ผูกกับ skill อื่น** — source → `skill-git-standard` · ตรวจก่อน promote → `skill-cybersecurity-container-iac` + secret-scan

## ผลลัพธ์ที่ได้จากการใช้งาน
- โครง `Dockerfile` + `docker-compose.yml` + `.dockerignore` ตามมาตรฐาน (multi-stage, non-root, no-secret)
- flow dev → GitHub → approve → BI promote (Docker Hub private → AWS prod) ที่ชัดเจน
- กัน credential หลุดเข้า image

## วิธีใช้
```
/skill-docker-standard
/skill-docker-standard            # เมื่อจะ containerize แอปใหม่
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อทำงานกับ Docker/compose/deploy

## ตัวอย่าง
```
user: "ทำให้ webapp นี้รันบน server ได้"
→ skill วาง Dockerfile (multi-stage) + docker-compose.yml + .dockerignore,
  ใส่ secret ผ่าน env_file, เตือน push source ขึ้น GitHub (ไม่ push image),
  ชี้ว่า BI จะ promote ขึ้น prod หลัง approve
```
