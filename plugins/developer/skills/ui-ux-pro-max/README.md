# ui-ux-pro-max

## Overview
Design intelligence engine สำหรับ UI/UX (web + mobile) — ฐานข้อมูล 50+ styles, 161 color palettes, 57 font pairings, 161 product types, 99 UX guidelines, 25 chart types ข้ามหลาย stack (Next.js, React, Vue, Svelte, Tailwind, shadcn, RN, Flutter ฯลฯ) ค้นผ่าน `scripts/search.py` ปรับให้เข้าธีม kob: **default = Next.js/web** (ตาม skill-architecture-standard)

## วิธีการคิดและการทำงานของ Skill
1. **วิเคราะห์ requirement** — product type / audience / style keywords / stack (default Next.js/web)
2. **`--design-system`** — สร้าง design system ครบ (pattern/style/สี/typography/effects + anti-patterns)
3. **`--domain`** — เจาะลึกราย domain (style, color, typography, ux, chart, landing ฯลฯ)
4. **`--stack`** — best practices ตาม stack (nextjs/react/html-tailwind ... )
5. ใช้คู่ **skill-frontend-web** (เลือก design → ลงมือ implement)

## ผลลัพธ์ที่ได้จากการใช้งาน
- Design system + palette + typography ที่มีเหตุผลรองรับ
- UX/accessibility checklist (priority 1→10)
- คำแนะนำ chart / layout / animation ตาม best practice

## วิธีใช้
```
python scripts/search.py "saas dashboard modern" --design-system --stack nextjs
python scripts/search.py "glassmorphism dark" --domain style
```
> รัน script จากโฟลเดอร์ skill นี้ · ต้องมี Python 3

## ตัวอย่าง
```
"ออกแบบ dashboard ให้ดูโปร"
→ --design-system → ได้ style/สี/ฟอนต์/effects + anti-patterns → ส่งต่อ skill-frontend-web เขียนโค้ด
```
