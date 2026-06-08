# Commit Message Convention — มาตรฐานข้อความ Commit

ใช้รูปแบบ **Conventional Commits** เพื่อให้ประวัติอ่านง่ายและ generate changelog อัตโนมัติได้

> Based on **Conventional Commits** for readable history and automated changelogs.

---

## 1. รูปแบบ (Format)

```
<type>(<scope>): <subject>
<บรรทัดว่าง / blank line>
<body — อธิบายว่าทำไม ไม่ใช่ทำอะไร / explain WHY, not WHAT>
<บรรทัดว่าง / blank line>
<footer — ref ticket / breaking change>
```

ตัวอย่าง (Example):
```
feat(auth): add Google OAuth login

ผู้ใช้สามารถล็อกอินด้วยบัญชี Google ได้ ลดขั้นตอนการสมัครสมาชิก
Allow users to sign in with Google to reduce signup friction.

Refs: JIRA-123
```

---

## 2. Type ที่ใช้ได้ (Allowed Types)

| Type | ใช้เมื่อ (When) |
|---|---|
| `feat` | เพิ่มฟีเจอร์ใหม่ (new feature) |
| `fix` | แก้บั๊ก (bug fix) |
| `docs` | แก้เอกสารอย่างเดียว (documentation) |
| `style` | format, เว้นวรรค ไม่กระทบ logic (formatting) |
| `refactor` | ปรับโครงสร้างโค้ด ไม่เพิ่ม feature/ไม่แก้บั๊ก |
| `perf` | ปรับ performance |
| `test` | เพิ่ม/แก้ test |
| `build` | ระบบ build, dependencies |
| `ci` | ไฟล์ CI/CD |
| `chore` | งานจิปาถะ ไม่กระทบ src/test |
| `revert` | ย้อน commit ก่อนหน้า |

---

## 3. กฎของ Subject (Subject Rules)

| ✅ ทำ (Do) | ❌ อย่าทำ (Don't) |
|---|---|
| ใช้ประโยคบอกเล่า/คำสั่ง: `add`, `fix`, `remove` | อดีตกาล: `added`, `fixed` |
| ไม่เกิน ~50 ตัวอักษร | ยาวเป็นย่อหน้า |
| ขึ้นต้นตัวพิมพ์เล็ก | `Add Feature` |
| ไม่ใส่จุดท้ายประโยค | `add feature.` |

---

## 4. ตัวอย่างจริง (Real Examples)

```bash
feat(payment): support PromptPay QR
fix(cart): prevent negative quantity
docs(readme): update setup instructions
refactor(api): extract user service
chore(deps): bump axios to 1.7.2
```

### Breaking change
```
feat(api): change auth response schema

BREAKING CHANGE: `token` field renamed to `accessToken`.
```

---

## 5. ตั้งค่า Template (Setup)

ไฟล์ [.gitmessage](../.gitmessage) เป็น template ที่จะเด้งขึ้นมาเวลา `git commit`

```bash
git config commit.template .gitmessage
```
