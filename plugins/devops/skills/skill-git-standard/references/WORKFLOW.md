# Workflow & Push Rules — ขั้นตอนการทำงานและกฎการ Push

เอกสารนี้อธิบายขั้นตอนการทำงานประจำวันและกฎการ push เพื่อให้ทุกคนในทีมทำงานเหมือนกัน

> Daily workflow and push rules so the whole team works the same way.

---

## 1. วงจรการทำงานต่อ 1 Feature (Lifecycle of one feature)

```
1. sync uat        →  2. สร้าง branch     →  3. เขียนโค้ด + commit
   (pull)              feature/<name>        (commit ย่อย ๆ บ่อย ๆ)
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
git checkout -b feature/user-login
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
git push -u origin feature/user-login   # ครั้งแรกใช้ -u
git push                                   # ครั้งถัดไป
```

### Step 5 — เปิด Pull Request เข้า `uat`
- เปิด PR บน GitHub: `feature/user-login` ──▶ `uat`
- ⚠️ **base ต้องเป็น `uat`** — GitHub default เป็น `main` ต้องเปลี่ยน dropdown เอง · **ห้าม PR `feature/* → main` ตรง (ห้ามข้าม UAT)**
- 🔗 **ใช้ลิงก์ที่ฝัง base=uat + title + body เสมอ:** `https://github.com/<org>/<repo>/compare/uat...<feature-branch>?expand=1&title=<TITLE>&body=<BODY>` (URL-encode ค่า · อย่าใช้ `…/pull/new/<branch>` ที่ default base = main · description ต้องเขียนทุกครั้ง)
- กรอกตาม PR template, ขอ reviewer, รอ approve
- merge แล้วลบ branch
- ✅ ขั้นนี้ **ผู้ช่วย/Claude ช่วยทำได้** (commit/push/เปิด PR เข้า uat)

### Step 6 — Promote `uat` → `main` (เมื่อ UAT ผ่าน)
- เปิด PR: `uat` ──▶ `main`
- ต้องผ่านการทดสอบบน UAT ก่อน
- 🤝 ขั้นนี้ **user กดเองเท่านั้น** — เป็น gate ขึ้น production · **ผู้ช่วย/Claude ห้ามเปิด/merge แทน** (ทำได้แค่เตรียม + ชี้ลิงก์)

---

## 3. กฎการ Push (Push Rules) 🚦

| # | กฎ (Rule) | คำอธิบาย (Why) |
|---|---|---|
| 1 | ❌ **ห้าม push ตรงเข้า `main`** (บังคับ) | ต้องผ่าน PR เสมอ — ล็อกด้วย GitHub Branch Protection. `uat` ใช้ PR ตามธรรมเนียมแต่ไม่บังคับ |
| 1.5 | 🚧 **ห้าม PR ข้าม UAT** | `feature/*` PR เข้า `uat` เท่านั้น (base = `uat`) · `uat → main` user กดเอง — ผู้ช่วยห้ามทำแทน |
| 2 | ✅ **push เฉพาะ `feature/*` ของตัวเอง** | แต่ละคนรับผิดชอบ branch ตัวเอง |
| 3 | ⚠️ **ห้าม `--force` บน shared branch** | ใช้ได้เฉพาะ `feature/*` ของตัวเอง และใช้ `--force-with-lease` |
| 4 | 🔄 **pull/rebase ก่อน push เสมอ** | ลด merge conflict |
| 5 | 🧪 **รันเทสต์/lint ก่อน push** | อย่า push โค้ดที่พังขึ้นไป |
| 6 | 🔐 **ห้าม commit secret** | password, API key, .env — ใช้ .gitignore |
| 7 | 🚨 **ตรวจ credential ก่อน commit เสมอ** | บังคับผ่าน [pre-commit hook](../hooks/pre-commit) — พบแล้วบล็อกเป็น CRITICAL ดู [SECURITY.md](SECURITY.md) |

### `--force` ที่ปลอดภัย (Safe force-push)
```bash
# ใช้ force-with-lease เสมอ — จะไม่ทับงานคนอื่นที่ push มาก่อน
git push --force-with-lease origin feature/user-login
```

---

## 4. เมื่อเกิด Merge Conflict (Handling conflicts)

```bash
# ดึง uat ล่าสุดมา rebase บน feature branch
git checkout feature/user-login
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
