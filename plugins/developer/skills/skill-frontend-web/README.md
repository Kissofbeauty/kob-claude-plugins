# skill-frontend-web

## Overview
skill **ความรู้/มาตรฐานการเขียน frontend** ของทีม — ใช้เป็นเกณฑ์ให้ subagent-fullstack (หรือ dev) เขียน/รีวิว UI ออกมาคุณภาพดี ครอบ **HTML, CSS, SCSS, Tailwind CSS, JavaScript, TypeScript, JSX/React** เน้น semantic + accessible, type-safe (no `any`), component เล็กทำหน้าที่เดียว, responsive mobile-first และไม่มีค่าลับในโค้ด frontend ไม่ใช่ tutorial แต่เป็นแนวทาง best-practice ที่บังคับใช้

## วิธีการคิดและการทำงานของ Skill
1. **a11y + semantic เป็นค่าเริ่มต้น** — เลือก tag ตามความหมาย, alt/label/heading/keyboard ครบ (ดีไซน์เชิงภาพอ้าง `ui-ux-pro-max`)
2. **Token เดียว สม่ำเสมอ** — สี/ระยะ/ฟอนต์ ผ่าน CSS variables หรือ `tailwind.config` ไม่ hardcode กระจาย
3. **Type-safe** — TypeScript `strict`, ห้าม `any`, type ที่ขอบเขต
4. **React ถูกหลัก** — hooks rules, dependency ครบ, `key` เสถียร, state ไม่ซ้ำซ้อน, perf เมื่อจำเป็น
5. **ผูกกับ skill อื่น** — design → `ui-ux-pro-max` · security/secret → `skill-cybersecurity` · backend API → `skill-fastapi`

## ผลลัพธ์ที่ได้จากการใช้งาน
- โค้ด frontend ที่ semantic, accessible, responsive, type-safe และ maintain ได้
- โครง styling ที่มี design token เป็น single source of truth
- React component ที่ออกแบบถูกหลัก ไม่มี pitfalls ที่พบบ่อย (key/effect/state)
- กันค่าลับหลุดเข้า bundle frontend

## วิธีใช้
```
/skill-frontend-web
/skill-frontend-web            # เมื่อจะเขียน/รีวิว UI
```
หรือถูกหยิบมาใช้อัตโนมัติเมื่อทำงานกับ HTML/CSS/SCSS/Tailwind/JS/TS/React

## ตัวอย่าง
```
user: "ทำหน้า login เป็น React + Tailwind"
→ skill วาง component เล็กที่ semantic (form/label/button จริง),
  ใช้ token จาก tailwind.config, props มี type ชัด (no any),
  hooks ถูกกฎ + key เสถียร, responsive mobile-first,
  ไม่ hardcode secret (เรียก API ผ่าน backend), อ้าง ui-ux-pro-max ด้านดีไซน์
```

## ไฟล์ในนี้
| ไฟล์ | เนื้อหา |
|---|---|
| `SKILL.md` | มาตรฐานหลัก: HTML · CSS/SCSS · Tailwind · JS/TS · JSX/React + Rules + References |
| `references/css-styling.md` | CSS/SCSS architecture · BEM · design tokens · responsive · Tailwind config/`@apply` |
| `references/js-react.md` | JS/TS modern patterns · type safety · React component/hooks/state/key/perf · pitfalls |
