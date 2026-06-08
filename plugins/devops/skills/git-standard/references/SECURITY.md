# Security — กฎความปลอดภัยก่อน Commit

> Security rules enforced before every commit.

---

## 🔴 กฎ CRITICAL: ตรวจ Credential ก่อน Commit เสมอ

**ทุกครั้งก่อน commit จะต้องตรวจสอบไฟล์ที่ stage ไว้ว่ามี credential หลุดเข้าไปหรือไม่
หากพบ ให้แจ้งเตือนระดับ `CRITICAL` และ "บล็อก" การ commit ทันที**

> Before every commit, staged files MUST be scanned for credentials.
> If any is found, raise a **CRITICAL** alert and **BLOCK** the commit.

กฎนี้บังคับใช้อัตโนมัติผ่าน [pre-commit hook](../hooks/pre-commit)

---

## 1. สิ่งที่ถือว่าเป็น Credential (ห้าม commit เด็ดขาด)

| ประเภท (Type) | ตัวอย่าง (Example) |
|---|---|
| Private key | `-----BEGIN RSA PRIVATE KEY-----` |
| AWS key | `AKIA...`, `ASIA...` |
| Google API key | `AIza...` |
| Slack / GitHub token | `xoxb-...`, `ghp_...` |
| JWT / Bearer token | `eyJ...`, `Authorization: Bearer ...` |
| รหัสผ่านฝังในโค้ด | `password = "..."` |
| Secret / API key ฝังในโค้ด | `api_key = "..."`, `client_secret = "..."` |

---

## 2. การติดตั้ง Hook (Install — ทำครั้งเดียวต่อ repo)

```bash
# ชี้ให้ git ใช้ hook จากโฟลเดอร์ hooks/ ของโปรเจกต์
git config core.hooksPath hooks
```

> ทางเลือก: ถ้าไม่อยากตั้ง `core.hooksPath` ก็ copy ไฟล์ไปที่ `.git/hooks/pre-commit` แล้ว `chmod +x` ได้

ตรวจว่าใช้งานได้:
```bash
git commit            # ถ้าไฟล์ที่ stage มี credential → จะถูกบล็อกพร้อมข้อความ CRITICAL
```

---

## 3. หน้าตาการแจ้งเตือนเมื่อพบ (Alert output)

```
🚨 CRITICAL: พบ credential ที่อาจหลุดเข้า commit / potential credential detected
   การ commit ถูกบล็อกไว้ / commit BLOCKED

  ● config/app.py  →  Hardcoded secret/API key
      12:+api_key = "sk-abcdef0123456789abcdef"
```

การ commit จะ **ไม่สำเร็จ** (exit 1) จนกว่าจะแก้

---

## 4. ต้องทำอะไรเมื่อถูกบล็อก (What to do)

1. ลบ credential ออกจากโค้ด → ย้ายไปไว้ใน `.env` / environment variable
2. ตรวจว่า `.env` อยู่ใน [.gitignore](../.gitignore) แล้ว
3. **ถ้า key หลุดออกไปแล้วจริง (เคย commit/push) ให้ revoke แล้วหมุน (rotate) key ใหม่ทันที** — การลบไฟล์เฉย ๆ ไม่พอ เพราะยังอยู่ใน git history

---

## 5. การข้ามการตรวจ (Bypass) — ใช้เมื่อจำเป็นจริง ๆ เท่านั้น

บางครั้งอาจเป็น false positive (เช่นตัวอย่างใน docs):

```bash
git commit --no-verify
```

> ⚠️ ใช้ `--no-verify` ต่อเมื่อ **มั่นใจ 100%** ว่าไม่ใช่ credential จริง
> ความรับผิดชอบตกอยู่ที่ผู้ commit

---

## 6. ข้อจำกัด (Limitations)

- Hook ตรวจด้วย regex ของ pattern ที่พบบ่อย — ไม่ครอบคลุม 100% ของ secret ทุกชนิด
- ไม่ใช่ข้ออ้างให้เลิกระวัง: **อย่าพิมพ์ credential ลงในโค้ดตั้งแต่แรก** คือทางที่ปลอดภัยที่สุด
- พิจารณาเสริมเครื่องมือระดับองค์กร เช่น `gitleaks` / `trufflehog` ใน CI สำหรับการสแกนเชิงลึก
