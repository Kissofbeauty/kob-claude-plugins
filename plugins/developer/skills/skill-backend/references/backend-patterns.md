# Backend Patterns — bad vs good

## Error shape (เดียวกันทั้งระบบ)
```json
{ "error": { "code": "VALIDATION_ERROR", "message": "Email is invalid", "details": [] } }
```
- ใช้ code ที่ client map ได้ · message อ่านรู้เรื่อง · ❌ ไม่ใส่ stack trace/internal

## Validation ที่ boundary
```ts
// ✅ ตรวจ input ด้วย schema ก่อนเข้า logic
const Body = z.object({ email: z.string().email(), qty: z.number().int().positive() });
const parsed = Body.safeParse(await req.json());
if (!parsed.success) return json({ error: { code: "VALIDATION_ERROR", message: "..." } }, 422);
```
❌ อย่าเชื่อ body ตรง ๆ: `const { qty } = await req.json(); db.order(qty)`

## Layering
```
// ❌ business rule + SQL ปนใน handler
export async function POST(req) {
  const b = await req.json();
  if (b.qty > stock) ...           // business rule ใน controller
  await sql`INSERT ... ${b.qty}`;  // SQL ใน controller
}

// ✅ แยกชั้น
// controller: validate → call service
const dto = validate(await req.json());
const order = await orderService.create(dto, user);   // business logic
// service: rule + เรียก repository
// repository: parameterized query (ดู skill-sql)
```

## Authorization (กัน BOLA / API1)
```ts
// ❌ เชื่อ id จาก client โดยไม่เช็ก owner
const order = await repo.findById(params.id);
// ✅ ผูก owner เสมอ
const order = await repo.findByIdForUser(params.id, user.id);
if (!order) return json({ error: { code: "NOT_FOUND" } }, 404);
```

## REST conventions
| สิ่ง | ใช้ |
|---|---|
| สร้าง | `POST /orders` → 201 + Location |
| อ่าน | `GET /orders/:id` → 200 / 404 |
| แก้ทั้งก้อน/บางส่วน | `PUT` / `PATCH` |
| ลบ | `DELETE` → 204 |
| validation fail | 422 · auth 401 · forbidden 403 · conflict 409 |
| list | pagination (cursor/keyset) + filter ที่กำหนดไว้ ไม่เปิดอิสระ |

## GraphQL
- schema-first · resolver บาง (เรียก service) · กัน N+1 ด้วย dataloader · จำกัด query depth/complexity

## Secret / config
```ts
const apiKey = process.env.PAYMENT_API_KEY;   // ✅ จาก env (allowlist secret — อ่านจาก env ไม่ใช่ค่าจริง)
// ❌ const apiKey = "sk_live_xxxxxxxxxxxx"   // allowlist secret (ตัวอย่างห้ามทำ)
```
> ก่อนส่ง: `/skill-cybersecurity-api` + secret-scan · data layer ดู `skill-sql` · Python backend ดู `skill-fastapi`
