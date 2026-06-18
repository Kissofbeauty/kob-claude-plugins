# Branching Strategy — มาตรฐานการใช้ Branch

โมเดลนี้เป็นแบบ **3 ชั้น (3-tier environment promotion)** โค้ดจะถูก promote จาก dev → uat → production ตามลำดับ

> A 3-tier environment-promotion model. Code is promoted dev → uat → production.

---

## 1. โครงสร้าง Branch (Branch Structure)

| Branch | Environment | สร้างมาจาก (Branched from) | ใครเขียนได้ (Who commits) | Branch Protection (GitHub) |
|---|---|---|---|---|
| `main` | 🟢 Production | — (branch หลัก / root) | ❌ ห้าม push ตรง / no direct push | ✅ **บังคับ / enforced** (PR + approve) |
| `uat` | 🟡 UAT | `main` | ผ่าน PR ตามธรรมเนียม / PR by convention | ➖ ไม่บังคับฝั่ง server / not enforced |
| `feature/<featureName>` | 🔵 Development | `uat` | ✅ developer | ➖ ไม่บังคับ / none |

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
   feature/login ●──●──●──┘
   (development)
```

**อ่านจากบนลงล่าง / Read top-to-bottom:**
1. `uat` แยกออกมาจาก `main`
2. `feature/<featureName>` แยกออกมาจาก `uat`
3. dev เสร็จ → PR merge `feature/*` → `uat`
4. UAT ผ่าน → PR merge `uat` → `main`

---

## 3. การตั้งชื่อ Feature Branch (Naming Convention)

รูปแบบ: `feature/<featureName>`

| ✅ ดี (Good) | ❌ ไม่ดี (Bad) | เหตุผล (Reason) |
|---|---|---|
| `feature/user-login` | `feature/Login` | ใช้ kebab-case ตัวพิมพ์เล็ก |
| `feature/payment-gateway` | `feature/fix` | ตั้งชื่อให้สื่อความหมาย |
| `feature/export-report-csv` | `report` | ต้องขึ้นต้นด้วย `feature/` |

> เคล็ดลับ / Tip: ใส่หมายเลข ticket ได้ เช่น `feature/JIRA-123-user-login`

---

## 4. ขั้นตอนแบบ Command (Step-by-step Commands)

### 4.1 เริ่ม feature ใหม่ (Start a new feature)

```bash
# อัปเดต uat ให้ล่าสุดก่อนเสมอ / always sync uat first
git checkout uat
git pull origin uat

# สร้าง feature branch จาก uat / branch from uat
git checkout -b feature/user-login
```

### 4.2 dev เสร็จ → ขึ้น UAT (Merge feature → uat)

```bash
# push feature branch ขึ้น remote
git push -u origin feature/user-login

# จากนั้นเปิด Pull Request:  feature/user-login  ──▶  uat
# (เปิดผ่านหน้าเว็บ GitHub แล้วรอ review/approve)
```

### 4.3 UAT ผ่าน → ขึ้น Production (Merge uat → main)

```bash
# เปิด Pull Request:  uat  ──▶  main
# ต้องผ่านการทดสอบบน UAT และได้รับ approve ก่อน merge
```

> ⚠️ **ขั้นนี้ user เป็นคนกดเอง** — เป็น gate เผยแพร่ขึ้น production. ผู้ช่วย/Claude **ห้ามเปิดหรือ merge PR `uat → main` แทน** (ทำได้แค่เตรียมให้ + ชี้ลิงก์)

---

## 5. กฎการ Merge (Merge Rules)

| กฎ (Rule) | รายละเอียด (Detail) |
|---|---|
| ❌ **ห้าม PR ข้าม UAT** | `feature/*` PR เข้า `uat` เท่านั้น — **ห้าม `feature/* → main` ตรง** (base PR ต้องเป็น `uat`; GitHub default เป็น `main` ต้องเปลี่ยนเอง). ทุกการเปลี่ยนแปลงต้องผ่าน uat ก่อนเสมอ |
| 🤝 **ใครทำขั้นไหน** | `feature/* → uat` = ผู้ช่วย/Claude ช่วยได้ · `uat → main` (prod) = **user กดเองเท่านั้น** ผู้ช่วยห้ามทำแทน |
| `main` ผ่าน PR เท่านั้น (บังคับ) | ห้าม `git push` ตรงเข้า `main` — ล็อกด้วย GitHub Branch Protection |
| `uat` ผ่าน PR (ตามธรรมเนียม) | ควร merge ผ่าน PR แต่ไม่ได้บังคับฝั่ง server |
| ต้อง review / Require review | PR เข้า `main` ต้องได้รับ approve อย่างน้อย 1 คน |
| Sync ก่อน merge / Sync first | rebase หรือ merge `uat` ล่าสุดก่อนเปิด PR เพื่อกัน conflict |
| ลบ branch หลัง merge / Clean up | ลบ `feature/*` หลัง merge **ทั้ง remote และ local** — remote: เปิด GitHub **Settings → General → Automatically delete head branches**; local: `git fetch --prune` + `git branch -d feature/<name>` |
| ห้ามใช้ branch เก่าต่อ / No stale reuse | แก้เพิ่มหลัง merge → **แตก branch ใหม่จาก `uat` ล่าสุด** เสมอ แล้ว merge เข้า `uat` อีกรอบ (อย่ารื้อ branch ที่ลบแล้วมาใช้ต่อ) |

---

## 6. การ Hotfix (กรณีฉุกเฉินบน Production)

หากต้องแก้ด่วนบน production:

```bash
git checkout main
git pull origin main
git checkout -b feature/hotfix-payment-bug   # แยกจาก main

# แก้เสร็จ → PR เข้า main → จากนั้น sync กลับลง uat ด้วย
```

> **สำคัญ / Important:** หลัง merge hotfix เข้า `main` แล้ว ต้อง merge `main` กลับลงมาที่ `uat`
> เพื่อให้ทุก environment มีโค้ดตรงกัน (keep environments in sync).
