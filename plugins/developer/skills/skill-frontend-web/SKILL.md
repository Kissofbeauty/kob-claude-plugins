---
name: skill-frontend-web
description: Frontend web engineering standard & knowledge for the team. Use when writing or reviewing frontend code — HTML, CSS, SCSS, Tailwind CSS, JavaScript, TypeScript, JSX/React — to produce semantic, accessible, type-safe, maintainable UI. มาตรฐาน/ความรู้สำหรับเขียน frontend ให้คุณภาพดี. Trigger on "เขียน frontend", "html/css/scss/tailwind/react/jsx", "frontend best practice", or "/skill-frontend-web".
allowed-tools: Read, Glob, Grep, Write, Edit
---

# skill-frontend-web — Frontend Web Engineering Standard

ความรู้และมาตรฐานการเขียน frontend ของทีม — ใช้เป็นเกณฑ์เมื่อเขียน/รีวิว HTML, CSS, SCSS, Tailwind, JS/TS, JSX/React

> หลักการ: **semantic + accessible เป็นค่าเริ่มต้น** · **type-safe (no `any`)** · **component เล็ก ทำหน้าที่เดียว** · **ค่าลับไม่อยู่ใน frontend** · **สม่ำเสมอ (consistency) สำคัญกว่ารสนิยมส่วนตัว**

นี่คือ skill **ความรู้/มาตรฐาน** ไม่ใช่ tutorial — เป้าหมายคือชี้แนวทางที่ถูกต้องให้ subagent-fullstack เขียนโค้ดออกมาดี ไม่ใช่สอนตั้งแต่ศูนย์

---

## 🧱 HTML — Semantic & Accessible

- ใช้ **semantic tag** ตามความหมาย: `<header> <nav> <main> <section> <article> <aside> <footer>` ไม่ใช่ `<div>` ทุกอย่าง
- หนึ่งหน้ามี `<h1>` เดียว และ heading ไล่ระดับ (h1→h2→h3) ไม่ข้ามเพื่อความสวย
- **a11y เป็นค่าเริ่มต้น ไม่ใช่ของแถม**: `alt` ทุกรูป, `label` ผูกกับ input (`for`/`id`), ปุ่มจริงใช้ `<button>` ไม่ใช่ `<div onClick>`
- ใช้ ARIA **เฉพาะเมื่อ semantic HTML ทำไม่ได้** (ARIA ที่ผิดแย่กว่าไม่ใส่) · รักษา keyboard focus order ให้ใช้ tab ได้
- form: ใช้ `<form>` จริง, input มี `name` + `type` ที่ถูก, validate ฝั่ง client เป็น UX ไม่ใช่ security
- รายละเอียด a11y/responsive เชิงดีไซน์ → อ้าง **`ui-ux-pro-max`**

## 🎨 CSS / SCSS — Architecture & Responsive

- **ตั้งชื่อ class แบบมีระบบ** (BEM หรือ utility) สม่ำเสมอทั้งโปรเจกต์ — เลี่ยง selector ลึกและ `!important`
- **Design tokens ผ่าน CSS custom properties** (`--color-*`, `--space-*`) เป็น single source of truth ของสี/ระยะ/ฟอนต์
- **Responsive: mobile-first** — เขียน base ก่อนแล้ว `min-width` ขึ้นไป · ใช้ `rem`/`%`/`clamp()` มากกว่า `px` คงที่
- Layout สมัยใหม่ใช้ **Flexbox / Grid** ไม่ใช่ float/positioning hack
- SCSS: ใช้ nesting แบบตื้น (≤3 ชั้น), แตกไฟล์เป็น partial (`_variables`, `_mixins`, `_components`), ใช้ `@use` แทน `@import` (deprecated)
- → patterns เต็ม: `references/css-styling.md`

## 💨 Tailwind CSS — Utility-First

- **Utility-first** ในไฟล์ component ได้ แต่เมื่อ class ซ้ำหลายที่ → ดึงเป็น **component** (React) หรือ `@apply` ใน layer ของตัวเอง
- กำหนด design token ใน **`tailwind.config`** (colors, spacing, fontFamily) — อย่าใช้ arbitrary value `[#1a2b3c]` เกลื่อนโค้ด ให้ตั้งใน config แทน
- อย่าผสม Tailwind กับ inline `style=` ที่ซ้ำซ้อน · จัดลำดับ class ให้สม่ำเสมอ (ใช้ prettier-plugin-tailwindcss)
- responsive ใช้ prefix `sm: md: lg:` แบบ mobile-first เหมือนหลัก CSS ด้านบน
- → patterns เต็ม: `references/css-styling.md`

## ⚙️ JavaScript / TypeScript — Modern & Type-Safe

- **Modern ES**: `const`/`let` (ไม่ `var`), arrow function, template literal, destructuring, optional chaining `?.`, nullish `??`, async/await (ไม่ callback hell)
- **TypeScript เป็นค่าเริ่มต้น** สำหรับโปรเจกต์ใหม่ — **`any` ต้องห้าม** ใช้ `unknown` + narrowing, generics, หรือ type ที่ถูกต้องแทน
- ตั้ง `strict: true` ใน tsconfig · พึ่ง type inference เมื่อชัดเจน, ใส่ type ที่ขอบเขต (พารามิเตอร์/return ของฟังก์ชัน public)
- เขียนฟังก์ชัน **pure + เล็ก** ทำหน้าที่เดียว · เลี่ยง mutate ของที่รับเข้ามา · จัดการ error ชัดเจน (อย่ากลืน error เงียบ ๆ)
- โมดูล: ใช้ ES module (`import`/`export`), แยก concern, ไม่ทิ้ง `console.log` ใน production
- → patterns เต็ม: `references/js-react.md`

## ⚛️ JSX / React — Component Design

- **Component เล็ก ทำหน้าที่เดียว** · function component + hooks เท่านั้น (ไม่ class) · ตั้งชื่อ PascalCase
- **Rules of Hooks**: เรียก hook ที่ top level เท่านั้น (ห้ามใน loop/condition/nested function) · ระบุ dependency array ของ `useEffect`/`useMemo`/`useCallback` ให้ครบและถูกต้อง
- **State**: ยกระดับ state เท่าที่จำเป็น, แยก local vs shared, derived state คำนวณตอน render อย่าเก็บซ้ำ
- **`key`** ใน list ต้องเสถียรและไม่ซ้ำ (ใช้ id จริง **ไม่ใช่ array index** เมื่อ list เรียง/แทรกได้)
- **Performance**: memo เมื่อพิสูจน์ว่าจำเป็น (อย่า premature), หลีกเลี่ยงสร้าง object/function ใหม่ใน prop โดยไม่จำเป็น, split bundle/lazy load หน้าหนัก
- side effect อยู่ใน `useEffect`/event handler — ไม่ทำใน render body
- → patterns เต็ม + pitfalls: `references/js-react.md`

---

## ✅ Rules (บังคับ)

| กฎ | รายละเอียด |
|---|---|
| **a11y first** | semantic tag, alt, label, keyboard ใช้ได้, contrast ผ่าน (อ้าง `ui-ux-pro-max`) |
| **No secret in frontend** | ห้าม hardcode API key/token/credential ในโค้ด frontend (ดูได้จาก bundle) — ใช้ env ฝั่ง build ที่ public ได้เท่านั้น, secret จริงอยู่ฝั่ง backend → ตรวจด้วย `skill-cybersecurity` |
| **No `any`** | TS ต้อง type ชัด, `strict: true`, ไม่ปิด lint |
| **Consistency** | ยึด convention เดียวกันทั้งโปรเจกต์ (ชื่อ, format, โครง) — มี ESLint + Prettier และทำตาม |
| **Responsive + mobile-first** | ทุก UI ต้องใช้งานได้บนจอเล็ก |

> ⚠️ ตัวอย่าง config/secret ใน references เป็น **placeholder** ไม่ใช่ค่าจริง

## เช็กก่อนปิดงาน
1. HTML semantic + a11y ผ่าน (alt/label/heading/keyboard)
2. CSS/Tailwind ใช้ token จากที่เดียว + responsive mobile-first
3. TS ไม่มี `any`, `strict: true`, ผ่าน lint
4. React: hooks rules ถูก, `key` เสถียร, ไม่มี side effect ใน render
5. ไม่มี secret/credential ในโค้ด frontend

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/css-styling.md` | CSS/SCSS architecture · BEM · design tokens · responsive · Tailwind config/`@apply` |
| `references/js-react.md` | JS/TS modern patterns · type safety · React component/hooks/state/key/perf · common pitfalls |

## เชื่อมโยง skill อื่น
- ดีไซน์/a11y/responsive เชิงภาพ → **`ui-ux-pro-max`**
- ตรวจ secret/ช่องโหว่ฝั่ง frontend → **`skill-cybersecurity`**
- งาน API ฝั่ง backend ที่ frontend เรียก → **`skill-fastapi`**
