---
name: skill-cybersecurity-secret-scan
description: Secret/credential leak scanner for code and git history. Use when user asks to "scan for secrets", "find hardcoded key", "secret scan", "ตรวจ credential หลุด", "สแกน secret", "หา hardcoded key", or "/skill-cybersecurity-secret-scan".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-cybersecurity-secret-scan — Secret & Credential Leak Scanner

เมื่อถูกเรียก ให้ค้นหา secret/credential ที่หลุดเข้ามาในโค้ด **และ git history** แล้วสรุปเป็น report พร้อม remediation playbook — **ทำครบทุก Phase ตามลำดับ**

> **Defensive-only:** หน้าที่คือ "ตรวจหา + บอกวิธีอุดรอยรั่ว" ไม่ใช่ใช้ secret ที่เจอ · **ไม่พิมพ์ค่า secret เต็ม** ทุกครั้ง mask เหลือหัว-ท้าย (เช่น `AKIA…7K4Q`)

---

## Phase 1: Discovery — หาไฟล์/พื้นผิวที่เสี่ยง

1. ผู้ใช้ระบุ path → scan ตามนั้น · ไม่ระบุ → ทั้ง repo ใน working directory
2. กวาดพื้นผิวที่ secret มักหลุด (ใช้ Glob):
   - **Source:** `*.py`, `*.js`, `*.ts`, `*.go`, `*.java`, `*.rb`, `*.php`, `*.cs`, `*.rs`
   - **Config:** `*.env*`, `*.yaml`/`*.yml`, `*.toml`, `*.ini`, `*.json`, `*.properties`, `*.config.*`
   - **Infra/CI:** `Dockerfile*`, `docker-compose*`, `.github/**`, `.gitlab-ci.yml`, `*.tf`
   - **Notebook/Log:** `*.ipynb`, `*.log`, `*.bak`, `*.sql`, dump files
3. เช็คว่าไฟล์ลับถูก ignore จริงไหม: อ่าน `.gitignore` แล้วเทียบ — ไฟล์ลับที่ "ยัง track อยู่" คือธงแดง (`git ls-files | grep -Ei 'env|secret|key'`)

---

## Phase 2: Scan working tree — ตาม pattern secret

ใช้ Grep หา pattern ใน **`references/secret-patterns.md`** ครอบให้ครบทุกชนิด:

- Cloud keys — **AWS** (`AKIA…`), **GCP** service-account JSON, **Azure** connection string
- Tokens — **GitHub** (`ghp_/gho_/ghs_`), **Slack** (`xox[baprs]-`), generic `bearer`/`api[_-]?key`
- **JWT** (`eyJ…` 3 ส่วนคั่นด้วยจุด)
- **Private key** (`-----BEGIN … PRIVATE KEY-----`)
- **DB connection string** (`postgres://user:pass@…`, `mongodb+srv://…`)
- **Generic high-entropy** — string ยาว random ที่อยู่หลัง `=`/`:` ในชื่อ field ที่สื่อความลับ (`password`, `secret`, `token`)

---

## Phase 3: Scan git history — secret ที่ลบไปแล้วยังอยู่

**สำคัญที่สุด:** ลบไฟล์ออกจาก working tree ไม่ได้ลบมันออกจาก history — ใครก็ตามที่ clone repo ได้ยังดึง secret เดิมกลับมาได้ ต้องสแกนทุก commit:

```bash
# หา blob ที่เคยมี pattern secret ทุก commit
git grep -nI -e 'AKIA[0-9A-Z]{16}' -e 'ghp_[0-9A-Za-z]{36}' \
  -e 'BEGIN .*PRIVATE KEY' $(git rev-list --all)

# ดูว่า secret ถูก add/ลบ commit ไหน (เจาะ field ลับ)
git log -p -S 'api_key' --all
git log -p --all -- path/to/suspect.env
```

- เจอใน history → บันทึก commit hash + ผู้ commit + วันที่ ลงใน report (ยัง mask ค่า)
- ไฟล์ที่ "ไม่มีใน working tree แล้วแต่อยู่ใน history" = ต้อง remediate เท่ากับที่ยังอยู่

---

## Phase 4: Classify + verify — ลด false positive

แต่ละ match จัดชนิด แล้วกรองตัวปลอมออกก่อนรายงาน:

- **Context:** อยู่ในไฟล์ test/fixture/example/docs หรือ comment "example" → likely false positive
- **Placeholder:** `xxxx`, `your-key-here`, `<REDACTED>`, `changeme`, ค่า dummy ซ้ำตัว → ตัดออก
- **Entropy:** string ที่ดูสุ่มจริง (entropy สูง, ความยาวตรงสเปกของ provider) → น้ำหนักสูงขึ้น
- **Allowlist:** ถ้าโปรเจกต์มี marker เช่นบรรทัดลงท้าย `allowlist secret` ให้ถือว่าตั้งใจยกเว้น
- จัดความมั่นใจ: **Confirmed** (รูปแบบตรง + entropy สูง + ไม่ใช่ตัวอย่าง) · **Suspected** · **Likely-FP**
- ให้คะแนนแบบ **อนุรักษ์นิยม:** ไม่แน่ใจระหว่าง Confirmed/Suspected ของ key จริง → เลือกฝั่งร้ายแรงกว่า

---

## Phase 5: Report + Remediation playbook

**Report** — ตาราง finding เรียงตามความร้ายแรง แต่ละแถวมี: ชนิด secret · `file:line` (อ้างของจริง) · ค่าที่ mask · อยู่ใน working tree / history (+ commit) · confidence

**Remediation playbook — ลบไฟล์เฉย ๆ ไม่พอ:**

1. **Revoke + Rotate ก่อนเสมอ** — เพราะ secret อยู่ใน history ไปแล้ว ต้องถือว่า "หลุดถาวร": ยกเลิก key เดิมที่ provider แล้วออกตัวใหม่ (AWS IAM, GCP SA, GitHub PAT, DB password) — ขั้นนี้สำคัญกว่าการล้าง history
2. **ล้าง history** — เอา blob ออกจากทุก commit ด้วย `git filter-repo --invert-paths --path <file>` หรือ BFG (`bfg --delete-files <file>` / `--replace-text`) แล้ว force-push + ให้ทุกคน re-clone
3. **ย้ายไป secret manager / `.env`** — เก็บค่าจริงใน secret manager (Vault, AWS Secrets Manager, GitHub Actions secrets) หรือ `.env` ที่อยู่ใน `.gitignore` แล้วโค้ดอ่านจาก env var
4. **ป้องกันซ้ำ** — เพิ่ม pre-commit secret gate (อ้าง `skill-git-standard`) + เติม pattern ลง `.gitignore`

---

## Rules

- ทำครบทุก Phase ห้ามข้าม โดยเฉพาะ **Phase 3 (git history)** · ไม่พบอะไรให้ระบุ "✅ No secrets found" พร้อมบอกว่าตรวจอะไรไป
- **อ้างไฟล์/บรรทัดจริง** เสมอ (`path:line` + commit hash ถ้าอยู่ใน history)
- **ไม่พิมพ์ค่า secret เต็ม** — mask เหลือหัว-ท้ายเสมอ
- **Defensive เท่านั้น** — ชี้รอยรั่ว + วิธีอุด ไม่ใช้/ไม่ทดสอบ secret ที่เจอกับระบบจริง
- กรอง false positive แบบอนุรักษ์นิยม: ถ้าสงสัยว่าเป็น key จริง รายงานไว้ก่อน

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/secret-patterns.md` | รายการ pattern ทุกชนิด (cloud/token/JWT/private key/DB/high-entropy) + ตัวอย่าง |
