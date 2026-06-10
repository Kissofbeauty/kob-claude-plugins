# Secret Patterns — รายการ pattern ที่ตรวจ

> **หมายเหตุสำคัญ:** ตัวอย่างในไฟล์นี้ใช้ **placeholder `<...>`** แทนค่าจริงโดยตั้งใจ
> เพื่อให้สื่อ "รูปแบบ (format)" โดย **ไม่มีค่าที่ตรงกับ token จริง** — กันทั้ง GitHub Push Protection และ credential scanner ของ repo จับ (ของจริงห้ามอยู่ใน repo เด็ดขาด)
> ใช้ **regex** (ในเครื่องหมาย `` ` ``) เป็นตัวตรวจหลัก · บรรทัดตัวอย่างกำกับ `allowlist secret` ไว้ด้วย

แต่ละชนิดมี: คำอธิบาย · regex สำหรับ Grep · ตัวอย่าง format (placeholder)

---

## 1. AWS Access Key
- **regex:** `AKIA[0-9A-Z]{16}` (access key id) · secret key = `[0-9a-zA-Z/+]{40}`
- format: `AKIA` + 16 ตัวพิมพ์ใหญ่/เลข · ตัวอย่าง `AKIA<16-uppercase-alnum>` allowlist secret
- secret key: `aws_secret_access_key = "<40-char-base64>"` allowlist secret

## 2. GCP Service Account Key
- **regex:** `"type":\s*"service_account"` + `"private_key":\s*"-----BEGIN PRIVATE KEY` allowlist secret
- format: ไฟล์ JSON มี `"private_key_id": "<40-hex>"` + `"private_key"` allowlist secret
- มักเป็นไฟล์ `*.json` ที่ commit เข้า repo โดยไม่ตั้งใจ

## 3. Azure Storage / Connection String
- **regex:** `AccountKey=[A-Za-z0-9+/=]{40,}` · `DefaultEndpointsProtocol=https;AccountName=`
- format: `DefaultEndpointsProtocol=https;AccountName=<name>;AccountKey=<88-char-base64>;` allowlist secret

## 4. GitHub Token
- **regex:** `gh[posru]_[0-9A-Za-z]{36,}` (PAT/OAuth/server/refresh/user-to-server)
- format: `ghp_<36-base62-chars>` · fine-grained: `github_pat_<long-base62>` allowlist secret

## 5. Slack Token
- **regex:** `xox[baprs]-[0-9A-Za-z-]{10,}`
- format: `xoxb-<digits>-<digits>-<24-base62>` allowlist secret
- webhook: `https://hooks.slack.com/services/<T-id>/<B-id>/<24-chars>` allowlist secret

## 6. JWT (JSON Web Token)
- **regex:** `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
- format: `<base64url-header>.<base64url-payload>.<base64url-signature>` (header ขึ้นต้น `eyJ`) allowlist secret
- หมายเหตุ: JWT ไม่เข้ารหัส payload — ระวังข้อมูลใน claim ด้วย

## 7. Private Key (RSA/EC/OpenSSH/PGP)
- **regex:** `-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY` allowlist secret
- format: บล็อก `BEGIN ... PRIVATE KEY` ... `END ... PRIVATE KEY` ครอบ base64 หลายบรรทัด allowlist secret

## 8. Database Connection String
- **regex:** `(postgres|postgresql|mysql|mongodb(\+srv)?|redis|amqp)://[^:\s]+:[^@\s]+@`
- format: `postgres://<user>:<password>@<host>:5432/<db>` allowlist secret
- format: `mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<db>` allowlist secret

## 9. Generic API Key / Secret (field-based)
- **regex:** `(?i)(api[_-]?key|secret|token|passwd|password|access[_-]?key)\s*[:=]\s*['"][^'"\s]{12,}['"]`
- format: `api_key = "<provider-prefix>_<random-value>"` allowlist secret
- format: `STRIPE_SECRET = "<rk-or-sk-prefix>_<random>"` allowlist secret

## 10. Generic High-Entropy String
- **เกณฑ์:** string ยาว ≥ 20 ตัว, mix ตัวพิมพ์ใหญ่/เล็ก/เลข/สัญลักษณ์, Shannon entropy สูง (~> 4.0 bits/char) ที่อยู่หลัง `=`/`:` ในชื่อ field สื่อความลับ
- format: `SESSION_SECRET=<30-char-high-entropy>` allowlist secret
- ลด false positive: ตัด hash/checksum/UUID/base64 ของ asset ที่ไม่ใช่ credential ออก

---

## Placeholder ที่ "ไม่ใช่" secret (ตัดทิ้งใน Phase 4)
- `xxxxxxxx`, `your-api-key-here`, `<YOUR_TOKEN>`, `changeme`, `REDACTED`, `dummy`, `example`
- ค่าใน path ที่มี `test/`, `fixture/`, `mock/`, `__tests__/`, `examples/`, `docs/`
