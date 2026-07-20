# precompact

## Overview
Custom command สำหรับ PM (skill-PM) ใช้ก่อนกด compact — บันทึก state ทั้งหมดที่จำเป็นลง `docs/pm-handoff.md` เพื่อให้หลัง compact แล้ว PM กลับมาทำงานต่อได้ไร้รอยต่อ ไม่ลืม flow, กฎที่ user กำหนด, และวิธีใช้ subagent/skill ของโปรเจกต์

## วิธีการคิดและการทำงานของ Skill
- กวาดจากบทสนทนาปัจจุบัน: งานที่ค้าง + ขั้นที่อยู่ในลำดับ orchestration, สิ่งที่ต้องทำต่อ, กฎที่ user เคาะกลางบทสนทนา (สำคัญที่สุด — ไม่มีบันทึกที่ไหน), roster subagent/skill ของโปรเจกต์
- เขียนทับ `docs/pm-handoff.md` (state ล่าสุดเสมอ) — เนื้อหาที่มีใน docs อื่นแล้วใช้ลิงก์แทน ไม่ copy ซ้ำ
- หลักคิด: เขียนให้ PM ที่ไม่เห็นบทสนทนาเดิมเลยอ่านแล้วทำงานต่อได้ทันที (= สภาพจริงหลัง compact)
- ฝั่ง skill-PM มีตัวเชื่อม 2 จุด: แนะนำ `/precompact` เชิงรุกเมื่อ context เหลือ < 10% และอ่าน `docs/pm-handoff.md` เป็น action แรกเมื่อถูกเรียกหลัง compact

## ผลลัพธ์ที่ได้จากการใช้งาน
- ไฟล์ `docs/pm-handoff.md` ที่สรุป state พร้อมทำงานต่อ
- ทำงานต่อหลัง compact ได้ทันทีด้วยการพิมพ์ `/skill-PM` — ไม่ต้องเล่าใหม่ ไม่ลืมกฎที่เคยสั่ง

## วิธีใช้
```
/precompact        # ก่อนกด compact
# → กด compact
# → พิมพ์ /skill-PM เพื่อทำงานต่อจากเดิม
```

## ตัวอย่าง
```
(context เหลือน้อย PM เตือนเอง) → /precompact → compact → /skill-PM
```
