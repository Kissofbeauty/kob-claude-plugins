# JavaScript / TypeScript / JSX / React — Patterns & Pitfalls

> เป้าหมาย: โค้ดที่ type-safe, อ่านง่าย, component เล็ก, ไม่มี bug จาก hooks/state ที่พบบ่อย

---

## JavaScript / TypeScript

### Modern ES

```ts
const { id, name } = user;                 // destructuring
const label = name ?? "guest";             // nullish coalescing
const city = user.address?.city;           // optional chaining
const items = list.map((x) => x.id);       // arrow + immutable transform
const data = await fetchUser(id);          // async/await ไม่ callback hell
```

- `const` เป็นค่าเริ่มต้น, `let` เมื่อต้อง reassign, **ไม่ใช้ `var`**
- แปลงข้อมูลด้วย `map`/`filter`/`reduce` แบบ immutable — อย่า mutate input
- จัดการ error ชัดเจน: `try/catch` รอบ await และไม่กลืน error เงียบ ๆ

### Type safety — no `any`

```ts
// ❌ any ปิดการตรวจสอบทั้งหมด
function parse(input: any) { return input.value; }

// ✅ unknown + narrowing
function parse(input: unknown): string {
  if (typeof input === "object" && input !== null && "value" in input) {
    return String((input as { value: unknown }).value);
  }
  throw new Error("invalid input");
}

// ✅ generic เมื่อ type ขึ้นกับ input
function first<T>(arr: T[]): T | undefined { return arr[0]; }
```

```jsonc
// tsconfig.json
{ "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true } }
```

- ใส่ type ที่ "ขอบเขต" (พารามิเตอร์/return ของฟังก์ชัน public, props) แล้วปล่อยให้ infer ภายใน
- ใช้ `interface`/`type` แทนการกระจาย shape ซ้ำ · ใช้ union + discriminant แทน flag หลายตัว

---

## React — Component & Hooks

### Component design

```tsx
type AvatarProps = { src: string; alt: string; size?: number };

export function Avatar({ src, alt, size = 40 }: AvatarProps) {
  return <img src={src} alt={alt} width={size} height={size} className="rounded-full" />;
}
```

- function component + hooks เท่านั้น (ไม่ class) · PascalCase
- component เล็ก ทำหน้าที่เดียว · props มี type ชัด · มี `alt`/label เพื่อ a11y

### Rules of Hooks

```tsx
// ❌ hook ใน condition — ผิดกฎ ทำให้ order เพี้ยน
if (open) { const [x, setX] = useState(0); }

// ✅ top level เสมอ
const [x, setX] = useState(0);
useEffect(() => {
  const handler = () => setX((v) => v + 1);
  window.addEventListener("resize", handler);
  return () => window.removeEventListener("resize", handler); // cleanup
}, []); // dependency ครบ + ถูกต้อง
```

- เรียก hook ที่ top level เท่านั้น (ไม่ใน loop/condition/nested function)
- `useEffect`/`useMemo`/`useCallback` ต้องระบุ dependency array ให้ครบและถูก (อย่า disable lint ทิ้ง)
- มี cleanup ใน effect ที่ subscribe/timer/listener

### State

```tsx
// derived state: คำนวณตอน render อย่าเก็บซ้ำใน state
const fullName = `${first} ${last}`;        // ✅ ไม่ใช่ useState

// ยก state ขึ้นเท่าที่จำเป็น — local ก่อน, shared เมื่อจำเป็น
```

- อย่าเก็บค่าที่คำนวณได้จาก props/state อื่นไว้ใน state (จะ desync)
- shared state เยอะ → context หรือ state manager · อย่า prop-drill ลึกเกิน

### key ใน list

```tsx
// ❌ index เป็น key เมื่อ list เรียง/แทรก/ลบได้ → reconcile ผิด
{items.map((it, i) => <Row key={i} {...it} />)}

// ✅ id เสถียร ไม่ซ้ำ
{items.map((it) => <Row key={it.id} {...it} />)}
```

### Performance (อย่า premature)

- `React.memo` / `useMemo` / `useCallback` ใช้เมื่อ "พิสูจน์" ว่ามีปัญหา re-render จริง
- เลี่ยงสร้าง object/array/function ใหม่ใน prop ทุก render โดยไม่จำเป็น
- หน้าหนัก → `React.lazy` + `Suspense` (code splitting)
- side effect อยู่ใน `useEffect`/event handler — **ไม่ทำใน render body**

---

## Security note (frontend)
- ห้าม hardcode API key/secret ในโค้ด frontend — bundle เปิดดูได้ (เช่น `const API_KEY = "sk-live-xxxx"` allowlist secret)
- ค่าที่ build เข้า frontend ถือว่า public เสมอ · secret จริงอยู่ฝั่ง backend
- กัน XSS: เลี่ยง `dangerouslySetInnerHTML`; ถ้าจำเป็นต้อง sanitize → ตรวจด้วย `skill-cybersecurity`

## Common pitfalls (สรุป)
- `any` ปิด type check ทั้งสาย → ใช้ `unknown`/generic
- dependency array ของ effect ไม่ครบ → bug stale closure
- index เป็น key ใน list ที่เปลี่ยนลำดับได้
- เก็บ derived state ซ้ำ → ค่าไม่ตรงกัน
- mutate props/state ตรง ๆ → React ไม่ re-render หรือ behavior เพี้ยน
- premature memoization → โค้ดซับซ้อนโดยไม่จำเป็น
