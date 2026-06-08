# Branching Strategy — มาตรฐานการใช้ Branch

โมเดลนี้เป็นแบบ **3 ชั้น (3-tier environment promotion)** โค้ดจะถูก promote จาก dev → uat → production ตามลำดับ

> A 3-tier environment-promotion model. Code is promoted dev → uat → production.

---

## 1. โครงสร้าง Branch (Branch Structure)

| Branch | Environment | สร้างมาจาก (Branched from) | ใครเขียนได้ (Who commits) | Branch Protection (GitHub) |
|---|---|---|---|---|
| `main` | 🟢 Production | — (branch หลัก / root) | ❌ ห้าม push ตรง / no direct push | ✅ **บังคับ / enforced** (PR + approve) |
| `uat` | 🟡 UAT | `main` | ผ่าน PR ตามธรรมเนียม / PR by convention | ➖ ไม่บังคับฝั่ง server / not enforced |
| `z-feature/<featureName>` | 🔵 Development | `uat` | ✅ developer | ➖ ไม่บังคับ / none |

> **กฎเหล็ก / Hard rule:** เข้า `main` ได้เฉพาะผ่าน Pull Request เท่านั้น และถูก **บังคับด้วย GitHub Branch Protection**
> Code enters `main` **only** through a Pull Request — enforced server-side via GitHub Branch Protection.
>
> ส่วน `uat` ให้ merge ผ่าน PR เป็นมาตรฐานการทำงาน แต่ **ไม่ได้ล็อกฝั่ง server** (ทีมยึดถือกันเองตามวินัย)
> `uat` uses PRs **by convention** but is **not** server-enforced.

---

## 2. แผนภาพ Flow (Promotion Flow Diagram)

```
                    ┌─────────────────────────────────────────────┐
                    │                                             │
   main ────●───────────────────────────────────────●──────────▶  (production)
   (prod)   │                                        ▲
            │ branch                                 │ PR (merge เมื่อ UAT ผ่าน)
            ▼                                        │
   uat  ────●───────────────●────────────────────────●──────────▶  (UAT)
            │               ▲
            │ branch        │ PR (merge เมื่อ dev เสร็จ)
            ▼               │
   z-feature/login ●──●──●──┘
   (development)
```

**อ่านจากบนลงล่าง / Read top-to-bottom:**
1. `uat` แยกออกมาจาก `main`
2. `z-feature/<featureName>` แยกออกมาจาก `uat`
3. dev เสร็จ → PR merge `z-feature/*` → `uat`
4. UAT ผ่าน → PR merge `uat` → `main`

---

## 3. การตั้งชื่อ Feature Branch (Naming Convention)

รูปแบบ: `z-feature/<featureName>`

| ✅ ดี (Good) | ❌ ไม่ดี (Bad) | เหตุผล (Reason) |
|---|---|---|
| `z-feature/user-login` | `z-feature/Login` | ใช้ kebab-case ตัวพิมพ์เล็ก |
| `z-feature/payment-gateway` | `z-feature/fix` | ตั้งชื่อให้สื่อความหมาย |
| `z-feature/export-report-csv` | `feature/report` | ต้องขึ้นต้นด้วย `z-feature/` |

> เคล็ดลับ / Tip: ใส่หมายเลข ticket ได้ เช่น `z-feature/JIRA-123-user-login`

---

## 4. ขั้นตอนแบบ Command (Step-by-step Commands)

### 4.1 เริ่ม feature ใหม่ (Start a new feature)

```bash
# อัปเดต uat ให้ล่าสุดก่อนเสมอ / always sync uat first
git checkout uat
git pull origin uat

# สร้าง feature branch จาก uat / branch from uat
git checkout -b z-feature/user-login
```

### 4.2 dev เสร็จ → ขึ้น UAT (Merge feature → uat)

```bash
# push feature branch ขึ้น remote
git push -u origin z-feature/user-login

# จากนั้นเปิด Pull Request:  z-feature/user-login  ──▶  uat
# (เปิดผ่านหน้าเว็บ GitHub แล้วรอ review/approve)
```

### 4.3 UAT ผ่าน → ขึ้น Production (Merge uat → main)

```bash
# เปิด Pull Request:  uat  ──▶  main
# ต้องผ่านการทดสอบบน UAT และได้รับ approve ก่อน merge
```

---

## 5. กฎการ Merge (Merge Rules)

| กฎ (Rule) | รายละเอียด (Detail) |
|---|---|
| `main` ผ่าน PR เท่านั้น (บังคับ) | ห้าม `git push` ตรงเข้า `main` — ล็อกด้วย GitHub Branch Protection |
| `uat` ผ่าน PR (ตามธรรมเนียม) | ควร merge ผ่าน PR แต่ไม่ได้บังคับฝั่ง server |
| ต้อง review / Require review | PR เข้า `main` ต้องได้รับ approve อย่างน้อย 1 คน |
| Sync ก่อน merge / Sync first | rebase หรือ merge `uat` ล่าสุดก่อนเปิด PR เพื่อกัน conflict |
| ลบ branch หลัง merge / Clean up | ลบ `z-feature/*` ออกหลัง merge เข้า `uat` แล้ว |

---

## 6. การ Hotfix (กรณีฉุกเฉินบน Production)

หากต้องแก้ด่วนบน production:

```bash
git checkout main
git pull origin main
git checkout -b z-feature/hotfix-payment-bug   # แยกจาก main

# แก้เสร็จ → PR เข้า main → จากนั้น sync กลับลง uat ด้วย
```

> **สำคัญ / Important:** หลัง merge hotfix เข้า `main` แล้ว ต้อง merge `main` กลับลงมาที่ `uat`
> เพื่อให้ทุก environment มีโค้ดตรงกัน (keep environments in sync).
