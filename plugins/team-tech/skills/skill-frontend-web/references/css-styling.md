# CSS / SCSS / Tailwind — Styling Patterns

> เป้าหมาย: style ที่ maintain ได้, สม่ำเสมอ, responsive, มี single source of truth ของ token

---

## Design Tokens (single source of truth)

กำหนดสี/ระยะ/ฟอนต์ที่เดียว แล้วอ้างต่อทั้งโปรเจกต์ — ใช้ CSS custom properties:

```css
:root {
  --color-primary: #2563eb;
  --color-text: #1f2937;
  --space-1: 0.25rem;
  --space-4: 1rem;
  --radius: 0.5rem;
  --font-sans: "Inter", system-ui, sans-serif;
}
[data-theme="dark"] {
  --color-text: #e5e7eb;
}
```

- เปลี่ยน theme/brand ที่เดียว · รองรับ dark mode ผ่าน attribute/`prefers-color-scheme`
- อย่า hardcode `#2563eb` กระจายในหลายไฟล์ — อ้าง `var(--color-primary)` เสมอ

## ตั้งชื่อ class — BEM (ตัวอย่าง)

```css
/* Block__Element--Modifier */
.card { }
.card__title { }
.card--featured { }
```

- เลี่ยง selector ลึก (`.a .b .c .d`) และ `!important` (สัญญาณว่า specificity พัง)
- ชื่อสื่อความหมายเชิงหน้าที่ (`.btn--danger`) ไม่ใช่เชิงรูปลักษณ์ (`.btn-red`)

## Responsive — mobile-first

```css
.container { padding: var(--space-4); }          /* base = mobile */
@media (min-width: 768px) {                       /* tablet ขึ้นไป */
  .container { max-width: 720px; margin-inline: auto; }
}
```

- เขียน base สำหรับจอเล็กก่อน แล้วเพิ่มด้วย `min-width`
- ใช้หน่วยยืดหยุ่น: `rem`, `%`, `clamp(1rem, 2vw, 1.5rem)` มากกว่า `px` คงที่
- Layout: **Flexbox** สำหรับแถว/คอลัมน์เดียว · **Grid** สำหรับ 2 มิติ

## SCSS — โครงและกฎ

```scss
// styles/_variables.scss
$breakpoints: (sm: 640px, md: 768px, lg: 1024px);

// styles/_mixins.scss
@mixin mq($key) {
  @media (min-width: map-get($breakpoints, $key)) { @content; }
}

// styles/components/_card.scss
@use "../variables" as v;
@use "../mixins" as m;

.card {
  padding: 1rem;
  &__title { font-weight: 600; }      // nesting ตื้น ≤ 3 ชั้น
  @include m.mq(md) { padding: 1.5rem; }
}
```

- ใช้ `@use` แทน `@import` (deprecated)
- แตกเป็น partial: `_variables`, `_mixins`, `_base`, `components/*`
- nesting ลึกสุด ~3 ชั้น เพื่อกัน specificity บวมและคลาสยาวเกิน

---

## Tailwind CSS

### config = แหล่ง token

```js
// tailwind.config.js
export default {
  content: ["./src/**/*.{html,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: { primary: "#2563eb", surface: "#f8fafc" },
      spacing: { 18: "4.5rem" },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] },
    },
  },
};
```

- ตั้ง brand token ใน `theme.extend` → ใช้ `bg-primary` `text-surface` ทั่วโปรเจกต์
- เลี่ยง arbitrary value เกลื่อนโค้ด เช่น `bg-[#2563eb]` `mt-[13px]` — ตั้งใน config แทนเพื่อความสม่ำเสมอ

### เมื่อ utility ซ้ำ → ดึงออก

```jsx
// ❌ ซ้ำหลายที่ ดูแลยาก
<button className="px-4 py-2 rounded bg-primary text-white font-medium hover:bg-blue-700">…</button>

// ✅ ทำเป็น component (React) — ใช้ซ้ำ + แก้ที่เดียว
function Button({ children, ...props }) {
  return (
    <button
      className="px-4 py-2 rounded bg-primary text-white font-medium hover:bg-blue-700"
      {...props}
    >
      {children}
    </button>
  );
}
```

หรือใช้ `@apply` ใน layer ของตัวเองเมื่อจำเป็น:

```css
@layer components {
  .btn-primary { @apply px-4 py-2 rounded bg-primary text-white font-medium; }
}
```

### กฎ Tailwind
- responsive แบบ mobile-first ด้วย prefix: `class="p-4 md:p-6 lg:p-8"`
- จัดลำดับ class สม่ำเสมอด้วย `prettier-plugin-tailwindcss`
- อย่าผสม `style={{...}}` ที่ทำซ้ำกับ utility — เลือกทางเดียว
- dark mode: ใช้ `dark:` variant คู่กับ token

---

## Anti-patterns
- ❌ inline `style=` กระจายค่าซ้ำ → ใช้ class/token
- ❌ `!important` แก้ specificity → จัดโครง selector ใหม่
- ❌ hardcode สี/ระยะหลายที่ → design token
- ❌ desktop-first แล้ว override ด้วย `max-width` เยอะ → mobile-first
- ❌ arbitrary value Tailwind เกลื่อน → ตั้งใน config
