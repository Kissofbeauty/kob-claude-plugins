---
name: skill-cybersecurity-supply-chain
description: Software supply chain security scanner for dependencies, lockfiles, and CI/CD. Use when user asks to "check dependencies", "ตรวจ dependency", "scan supply chain", "ตรวจ supply chain", "SCA", "dependency audit", "ตรวจ CVE dependency", or "/skill-cybersecurity-supply-chain".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-cybersecurity-supply-chain — Software Supply Chain Security Scanner

เมื่อถูกเรียก ให้ทำ supply chain security assessment แล้วสรุปเป็น report — **ทำครบทุก Phase ตามลำดับ**

> **Stack-agnostic:** detect ecosystem ของ target ก่อน (npm / pip / go / maven / composer / gem / cargo / nuget) แล้วปรับการ scan ให้เข้ากับ ecosystem นั้น — ไม่ผูกภาษาใดภาษาหนึ่ง

---

## Phase 1: Discovery — หา manifest + lockfile ทุก ecosystem

1. ผู้ใช้ระบุ path/โฟลเดอร์ → scan ตามนั้น · ไม่ระบุ → ทั้ง project ใน working directory
2. **Detect ecosystem** จาก manifest + lockfile (อาจมีหลาย ecosystem ใน repo เดียว — หาให้ครบ):

   | Ecosystem | manifest | lockfile |
   |---|---|---|
   | npm/Node | `package.json` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
   | pip/Python | `requirements*.txt`, `pyproject.toml`, `Pipfile` | `poetry.lock`, `Pipfile.lock`, `requirements.lock` |
   | Go | `go.mod` | `go.sum` |
   | Maven/Gradle | `pom.xml`, `build.gradle` | `gradle.lockfile` |
   | Composer/PHP | `composer.json` | `composer.lock` |
   | RubyGems | `Gemfile`, `*.gemspec` | `Gemfile.lock` |
   | Cargo/Rust | `Cargo.toml` | `Cargo.lock` |
   | NuGet/.NET | `*.csproj`, `packages.config` | `packages.lock.json` |

3. อ่าน **CI/CD surface** ด้วย: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Dockerfile`, `*.sh` build scripts
4. รายละเอียด field/รูปแบบของแต่ละ ecosystem → ดู **`references/supply-chain-patterns.md`**

---

## Phase 2: Dependency Tree — direct + transitive

- แยก **direct dependencies** (จาก manifest) ออกจาก **transitive** (จาก lockfile)
- นับจำนวน, ระบุ depth, mark packages ที่มาจาก source/registry นอกมาตรฐาน
- ถ้ามี tool ในเครื่อง (เช่น `npm ls`, `pip list`, `go list -m all`) ใช้ช่วยยืนยัน tree ได้ — แต่ห้ามติดตั้ง/แก้ dependency

## Phase 3: Known CVE — เทียบ version

- เทียบ version ที่ pin จริง (จาก lockfile ถ้ามี ไม่งั้นจาก manifest) กับ known-vulnerable ranges
- **runtime/framework ก่อน** (Node · Next.js/React · Python · Starlette/FastAPI · PostgreSQL · Docker · OpenSSL · CA bundle) → เทียบกับ **`security-advisory-digest-2026.md`** (อยู่ใน `skill-cybersecurity/references/`) ซึ่งสรุป patched version + EOL จากแหล่ง official · EOL = High เสมอ
- รายงานเป็น `package@version → CVE-ID (severity) → fixed-in`
- ไม่มี network → อ้าง digest + ความรู้ที่มี แล้ว mark `ต้องยืนยันด้วย advisory DB` อย่างชัดเจน · conservative

## Phase 4: Typosquatting + Dependency Confusion

- **Typosquatting:** ชื่อ package คล้ายของดังแบบผิดเล็กน้อย (`reqeusts`, `lodahs`, `expresss`)
- **Dependency confusion:** ชื่อ package ภายในองค์กรที่อาจชนกับ public registry / ไม่ได้ pin scope/registry
- ดู indicator + ตัวอย่าง → `references/supply-chain-patterns.md`

## Phase 5: Pinning & Integrity

- หา unpinned/loose ranges (`>=`, `^`, `~`, `*`, `latest`) — เสี่ยงดึง version ที่ถูก compromise
- lockfile มีครบทุก ecosystem หรือไม่ · committed เข้า git หรือไม่
- integrity/hash: `integrity` (npm), `--hash` (pip), `go.sum`, checksum อื่น ๆ มีและตรงหรือไม่
- **cooldown:** มี `min-release-age` (npm ≥ 11.10) / `minimumReleaseAge` (pnpm) / Renovate `minimumReleaseAge` หรือไม่ — ไม่มี = Medium (worm ปี 2026 ทุก wave ถูกถอนภายใน 1–3 วัน)

## Phase 6: Malicious Install Scripts

- npm: `preinstall`/`install`/`postinstall` ใน `scripts` ที่รัน arbitrary code
- pip: `setup.py` ที่รันโค้ดตอน install / `cmdclass` override
- build/CI: `curl ... | bash`, `wget ... | sh`, `eval` จาก network, การ download binary แล้วรันทันที
- mark ทุกจุดที่ download+execute โดยไม่ verify checksum/signature
- **worm indicator (Shai-Hulud family 2025–2026):** `postinstall` ที่เรียก `bundle.js` / `setup_bun.js` / network, ไฟล์ workflow `.github/workflows/*.yml` ที่โผล่ใน package หรือถูก bot commit, version ใหม่ที่ไม่มี git tag/commit คู่กัน, wheel ที่มี `.pth` — ดู §2 ของ digest · ถ้าเจอ: ลำดับแก้ = ปิด persistence → rotate credential → reinstall (rotate ก่อนปิด = payload ลบ home directory)

## Phase 7: CI/CD Supply Chain

- GitHub Actions ที่ pin ด้วย tag/branch (`@v4`, `@main`) แทน commit SHA → mutable
- third-party actions จาก source ที่ไม่ verify · secrets ที่ส่งให้ step ภายนอก · action ที่เคยถูก compromise (`aquasecurity/trivy-action` มี.ค. 2026, `actions-cool/*` พ.ค.+ก.ย. 2026, `tj-actions/changed-files`) → ต้องเป็น SHA ที่สะอาด
- `pull_request_target` + checkout โค้ดจาก PR (ต้นเหตุ Trivy/TanStack ถูกยึด) · cache poisoning ข้าม workflow · OIDC token ที่รั่วจาก runner
- **publish credential:** ยังใช้ npm classic token / long-lived `NPM_TOKEN`, PyPI API token แบบไม่หมดอายุ → เสนอ **Trusted Publishing (OIDC)** + `--provenance` (config ใน §3 ของ digest)
- base image ใน Dockerfile ที่ใช้ `:latest` หรือไม่ pin digest (`@sha256:...`) · base image line ที่ EOL (เช่น `node:20`, `python:3.10`, `postgres:14`)

## Phase 8: SBOM + Report

ทำตามเทมเพลตใน `references/supply-chain-patterns.md`:
- **SBOM** — ตาราง component: name · version · ecosystem · direct/transitive · license (ถ้าทราบ)
- **Findings** — เรียง severity สูง→ต่ำ: finding · location (ไฟล์:บรรทัด) · evidence · remediation
- **Remediation Roadmap** — จัด priority + working config ที่ใช้ได้จริง

---

## Rules

- ทำครบทุก Phase ห้ามข้าม · ไม่พบในหมวดใดให้ระบุ "✅ No issues found" พร้อมบอกว่าตรวจอะไรไป
- **Defensive เท่านั้น:** ชี้ความเสี่ยง + วิธีแก้/hardening — ไม่เขียน exploit หรือ malicious package พร้อมใช้
- อ้าง **ไฟล์ + line number จริง** เสมอ (เช่น `package.json:23`)
- remediation ต้องเป็น **working config** (pinned version จริง, SHA จริง, lock command จริง) ไม่ใช่ pseudo
- ให้คะแนนแบบ **อนุรักษ์นิยม**: ไม่แน่ใจระหว่าง High/Medium → เลือก High · CVE ที่ยืนยันไม่ได้ → mark ชัดเจน
- **ห้ามแก้/ติดตั้ง/อัปเดต dependency จริง** — อ่านและรายงานเท่านั้น

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/supply-chain-patterns.md` | รายละเอียดต่อ ecosystem: pinning, lockfile, install-script field, dependency-confusion, CVE-prone packages, cooldown/trusted publishing, การอ่าน SBOM |
| `../skill-cybersecurity/references/security-advisory-digest-2026.md` | patched version + EOL ของ runtime/framework, incident ปี 2026 (Shai-Hulud, Trivy, PyPI), severity mapping, working config |
