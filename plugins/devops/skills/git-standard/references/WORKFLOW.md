# Workflow & Push Rules — ขั้นตอนการทำงานและกฎการ Push

เอกสารนี้อธิบายขั้นตอนการทำงานประจำวันและกฎการ push เพื่อให้ทุกคนในทีมทำงานเหมือนกัน

> Daily workflow and push rules so the whole team works the same way.

---

## 1. วงจรการทำงานต่อ 1 Feature (Lifecycle of one feature)

```
1. sync uat        →  2. สร้าง branch     →  3. เขียนโค้ด + commit
   (pull)              z-feature/<name>        (commit ย่อย ๆ บ่อย ๆ)
                                                       │
6. merge → main    ←  5. PR → uat          ←  4. push branch
   (UAT ผ่าน)          (dev เสร็จ)              (origin)
```

---

## 2. ขั้นตอนละเอียด (Detailed Steps)

### Step 1 — Sync ก่อนเริ่มเสมอ (Always sync first)
```bash
git checkout uat
git pull origin uat
```

### Step 2 — สร้าง feature branch (Create feature branch)
```bash
git checkout -b z-feature/user-login
```

### Step 3 — เขียนโค้ดและ commit (Code & commit)
```bash
git status                 # ดูว่ามีอะไรเปลี่ยน
git add <file>             # เลือกไฟล์ที่จะ commit (อย่าใช้ git add . พร่ำเพรื่อ)
git commit                 # เปิด editor ตาม .gitmessage template
```
> ดูรูปแบบข้อความ commit ที่ [COMMIT_CONVENTION.md](COMMIT_CONVENTION.md)

### Step 4 — Push branch ขึ้น remote (Push)
```bash
git push -u origin z-feature/user-login   # ครั้งแรกใช้ -u
git push                                   # ครั้งถัดไป
```

### Step 5 — เปิด Pull Request เข้า `uat`
- เปิด PR บน GitHub: `z-feature/user-login` ──▶ `uat`
- กรอกตาม PR template, ขอ reviewer, รอ approve
- merge แล้วลบ branch

### Step 6 — Promote `uat` → `main` (เมื่อ UAT ผ่าน)
- เปิด PR: `uat` ──▶ `main`
- ต้องผ่านการทดสอบบน UAT ก่อน

---

## 3. กฎการ Push (Push Rules) 🚦

| # | กฎ (Rule) | คำอธิบาย (Why) |
|---|---|---|
| 1 | ❌ **ห้าม push ตรงเข้า `main`** (บังคับ) | ต้องผ่าน PR เสมอ — ล็อกด้วย GitHub Branch Protection. `uat` ใช้ PR ตามธรรมเนียมแต่ไม่บังคับ |
| 2 | ✅ **push เฉพาะ `z-feature/*` ของตัวเอง** | แต่ละคนรับผิดชอบ branch ตัวเอง |
| 3 | ⚠️ **ห้าม `--force` บน shared branch** | ใช้ได้เฉพาะ `z-feature/*` ของตัวเอง และใช้ `--force-with-lease` |
| 4 | 🔄 **pull/rebase ก่อน push เสมอ** | ลด merge conflict |
| 5 | 🧪 **รันเทสต์/lint ก่อน push** | อย่า push โค้ดที่พังขึ้นไป |
| 6 | 🔐 **ห้าม commit secret** | password, API key, .env — ใช้ .gitignore |
| 7 | 🚨 **ตรวจ credential ก่อน commit เสมอ** | บังคับผ่าน [pre-commit hook](../hooks/pre-commit) — พบแล้วบล็อกเป็น CRITICAL ดู [SECURITY.md](SECURITY.md) |

### `--force` ที่ปลอดภัย (Safe force-push)
```bash
# ใช้ force-with-lease เสมอ — จะไม่ทับงานคนอื่นที่ push มาก่อน
git push --force-with-lease origin z-feature/user-login
```

---

## 4. เมื่อเกิด Merge Conflict (Handling conflicts)

```bash
# ดึง uat ล่าสุดมา rebase บน feature branch
git checkout z-feature/user-login
git fetch origin
git rebase origin/uat

# แก้ conflict ในไฟล์ แล้ว
git add <ไฟล์ที่แก้แล้ว>
git rebase --continue

# push (ต้อง force-with-lease เพราะ history เปลี่ยน)
git push --force-with-lease
```

> ถ้า rebase พัง อยากเลิก: `git rebase --abort`

---

## 5. Checklist ก่อนเปิด PR (Pre-PR Checklist)

- [ ] โค้ดรันผ่าน / build ได้ (code builds)
- [ ] รันเทสต์ผ่าน (tests pass)
- [ ] ไม่มี secret / credential / debug log หลงเหลือ (pre-commit hook ตรวจให้แล้ว)
- [ ] commit message ตรงตามมาตรฐาน
- [ ] sync `uat` ล่าสุดแล้ว ไม่มี conflict
- [ ] กรอก PR description ครบ
