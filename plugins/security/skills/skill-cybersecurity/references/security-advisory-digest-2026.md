# Security Advisory Digest — 2026 (ข้อมูล ณ 2026-10-24)

สรุป advisory จาก **แหล่ง official** ของ stack ที่องค์กรใช้ (ดู `skill-architecture-standard`) เพื่อให้ทุก skill-cybersecurity* และ subagent-cybersecurity-auditor ใช้ **เทียบ version ที่ detect ได้ → ชี้ finding** ได้ทันทีโดยไม่ต้องเดา

> **วิธีใช้:** detect version จริงจาก lockfile / `Dockerfile` / `.nvmrc` / `pyproject.toml` / `node -v` / `pg_config --version` → เทียบกับคอลัมน์ **patched** และ **EOL** ด้านล่าง → ต่ำกว่า patched = finding (severity ตาม §4) · runtime ที่ EOL = finding **High** เสมอ
> **อายุข้อมูล:** ไฟล์นี้ต้อง refresh **เดือนละครั้ง** หรือเมื่อมี advisory Critical/High ใหม่ · ถ้าวันที่หัวไฟล์เก่ากว่า 45 วัน ให้ mark ใน report ว่า "digest อาจไม่ครบ — ยืนยันกับ advisory DB (GHSA/OSV/NVD)"

---

## 1. Runtime & Framework — patched version / EOL

| Component | Patched (ต่ำกว่านี้ = finding) | EOL / status | ประเด็นสำคัญ 2026 |
|---|---|---|---|
| **Node.js** | **26.12.1** · **24.22.1** · **22.23.4** (2026-10-21) | 20 = **EOL 2026-04-30** (ห้ามใช้) · 22 Maintenance → EOL 2027-04-30 · 24 Maintenance ตั้งแต่ 2026-10-20 → EOL 2028-04-30 · 26 เป็น LTS **2026-10-28** → EOL 2029-04-30 · ตั้งแต่ 27 ออกปีละครั้ง ทุกตัวเป็น LTS | Oct 2026: 10 CVE (High 4) — **CVE-2026-111497 Brotli decoder OOB write → RCE** (ทุก app ที่ decompress ข้อมูลภายนอกด้วย `node:zlib` รวม `fetch()` / Express 5 auto-decompress) · TLS hostname bypass **CVE-2026-105483 / 106069 / 106072** (fullwidth digit, leading-zero, non-canonical IPv4) · `dns.resolve*` NUL truncation CVE-2026-105482 · keep-alive response smuggling CVE-2026-105481 · **CVE-2026-106074** entropy cache ติดไปใน startup snapshot/SEA → `randomUUID()` / `randomInt()` ซ้ำ — **ต้อง rebuild snapshot/SEA หลังอัปเกรด** · permission-model bypass (26.x) |
| **Next.js** | **16.4.1** (Active LTS) · **15.5.28** (Maintenance LTS) (2026-10-14) · ≤14.x ไม่ได้รับ patch | ตั้งแต่ ก.ค. 2026 มี **scheduled security release รายเดือน** (pre-announce บน nextjs.org/blog) + out-of-band เมื่อ Critical | Oct 14: **GHSA-673q-mjm6-r5xr Critical RCE** `use cache` คืน typed arrays (ไม่มี workaround) · **CVE-2026-96889 Critical RCE** Image Optimization + SVG (workaround: `sharp` ≥ 0.35.5) · GHSA-p3m5-59mp-jv5r High DoS Server Actions · Sep 30 (16.3.8/15.5.27): CVE-2026-94483 SSRF image optimization (`remotePatterns`), CVE-2026-94543/94484 cache poisoning SSG/ISR **self-hosted**, CVE-2026-94544 Draft Mode leak, CVE-2026-94486 dev-server MCP endpoint leak · Sep 22: **CVE-2026-94545 Critical RCE** `next/og` ImageResponse (16.3.6/15.5.26) · Aug: CVE-2026-75604 Windows path traversal + AVIF/libheif RCE · Jul: CVE-2026-64642 middleware/proxy auth bypass (16.0–16.2.10) · Dec 2025: **CVE-2025-66478 "React2Shell"** RSC RCE |
| **React** (upstream ของ Next.js) | ตามที่ Next.js patched ดึงมา | — | GHSA-xqc2-xf4c-x3h3 (RCE typed arrays) · GHSA-h3gv-c5rc-p453 (DoS) · RSC protocol (React2Shell) — app ที่ใช้ React Server Components นอก Next.js ต้องอัป React เอง |
| **Python** | **3.15.1** · **3.14.9** (bugfix) · **3.13.17** · **3.12.15** · **3.11.17** (security-only) (ต.ค. 2026) | **3.10 EOL 2026-10-01** · 3.9 EOL 2025-10-31 · 3.11 EOL 2027-10 · 3.12 EOL 2028-10 · 3.13 EOL 2029-10 | coordinated release 2026-10-01 แก้ 7 CVE ทุก branch (+ `tarfile` CVE-2026-87910) · base image `python:3.10*` / `3.9*` = EOL |
| **FastAPI / Starlette** | FastAPI **0.162.0** (2026-10-23) · **Starlette ≥ 1.3.1** | — | **CVE-2026-54283 High** DoS — `request.form()` ไม่บังคับ `max_fields` / `max_part_size` กับ urlencoded (fix 1.3.1) · **CVE-2026-48818 High** StaticFiles บน Windows เปิด SMB ไป UNC host → NTLM leak/SSRF (fix 1.1.0) · **CVE-2026-48710 "BadHost"** Host header ทำ `request.url.path` ผิด → bypass path-based auth ใน middleware (fix 1.0.1; `Depends()` ของ FastAPI ไม่กระทบ) · GHSA-x746-7m8f-x49c HTTPEndpoint dispatch method ผ่าน `getattr` · เช็คจริงด้วย `pip show starlette` |
| **PostgreSQL** | **18.6** · **17.11** · **16.15** · **15.19** · **14.24** (2026-08-13) · minor ถัดไปคาด พ.ย. 2026 | **14 EOL 2026-11-12** · ≤13 EOL แล้ว (ไม่ได้ fix ปี 2026 เลย) | ปี 2026 มี **44 CVE**, หลายตัว CVSS 8.8 RCE: regexp CVE-2026-14664, `to_char` CVE-2026-14669, plperl CVE-2026-14670, refint CVE-2026-14671, tsvector CVE-2026-14662, pg_dump client CVE-2026-19385, psql unrestrict CVE-2026-18408 · **pgcrypto เข้ารหัสเป็น cleartext เงียบ ๆ** เมื่อ cipher ถูก OpenSSL ปิด CVE-2026-14663 · row security cache ไม่สน role change CVE-2026-14666 · SQLi: REFRESH PUBLICATION CVE-2026-6638, pg_createsubscriber CVE-2026-6476, EXTRACT deparse CVE-2026-15741 |
| **Docker Engine / Desktop** | Engine **29.9.2** (2026-10-20) · Desktop **≥ 4.86.0** · Sandboxes ≥ 0.42.0 | — | **CVE-2026-34040 AuthZ plugin bypass (8.8)** — fix ไม่สมบูรณ์ของ CVE-2024-41110 → Engine 29.3.1 / Desktop 4.66.1 · `docker cp` host write/TOCTOU CVE-2026-41567/41568/42306 → 29.5.1 · **CVE-2026-17106** `docker cp` escape (มี PoC สาธารณะ) → 29.7.0 / Desktop 4.86.0 · 29.8.2 แก้ overlay network forged frame + TLS fallback ผ่าน DNS + BuildKit cache poisoning · 29.9.0–29.9.1 Go HTTP/2 DoS + containerd 2.4.2 · 29.9.2 ปฏิเสธ eMudhra CA (ดูแถวล่าง) · Model Runner container→host RCE CVE-2026-5817/5843 → Desktop 4.68/4.71 |
| **OpenSSL** (ใน base image / Python / Node) | **3.5.9** (LTS, 2026-09-29) · 3.6.5 · 3.0.23 | **3.5 = LTS ถึง 2030-04-08** · 3.6 EOL 2026-11-01 · 3.4 EOL 2026-10-22 · **3.0 หมด support** (extended เท่านั้น) · 1.1.1 EOL | Sep 2026: **CVE-2026-84782 High** DTLS retransmission · Aug: CMS key unwrap heap overflow CVE-2026-63072, QUIC double free · Jun: 3.5.7 แก้ 15 CVE (CMS forgery, PKCS7_verify UAF CVE-2026-45447 มี PoC) · Jan: CVE-2025-15467 CMS stack overflow |
| **CA trust store** | `ca-certificates` / `certifi` / Go runtime ล่าสุด (หลัง 2026-10-17) | — | **eMudhra: private key ของ intermediate CA 8 ใบหลุด** (เปิดเผย 2026-10-17) — Chrome/Firefox/Apple/Microsoft block แล้ว แต่ **client ที่ไม่ใช่ browser** (Go, Python `certifi`, Node, trust store ที่ bundle มากับ image/appliance) ต้องอัปเดตเอง → rebuild image ให้ได้ `ca-certificates` ใหม่ · Docker Engine 29.9.2 · pin `certifi` ล่าสุด |

---

## 2. Supply-chain incidents 2026 — สิ่งที่ scanner ต้องรู้

| เมื่อไร | เหตุการณ์ | บทเรียน / สิ่งที่ต้องตรวจ |
|---|---|---|
| ก.ย. 2025 → พ.ย. 2025 → **พ.ค. 2026** → **ส.ค. 2026** | **Shai-Hulud worm** (npm): original → "2.0" → **Mini Shai-Hulud** (TanStack, AntV, Mistral; 170+ npm + 2 PyPI; เข้าทาง GitHub Actions "pwn request" + cache poisoning + ดึง OIDC token จาก runner) → **CHAINDROP** (maintainer ของ `keyv` ถูกยึด GitHub → backdoor 400+ package) · payload ขโมย npm/GitHub token, SSH key, cloud credential, **config ของ AI tool** แล้ว republish ตัวเองไปทุก package ที่ token publish ได้ · มี persistence ที่ **ทำลาย home directory ถ้า rotate credential ก่อนปิด service** | ลำดับ remediation สำคัญ: ปิด persistence → rotate → reinstall · indicator: `postinstall` ใหม่ + ไฟล์ `bundle.js` / `setup_bun.js`, workflow `.github/workflows/*.yml` ที่ bot เพิ่ม, version ใหม่ที่ **ไม่มี git tag/commit คู่กัน**, publish นอก CI (ไม่มี provenance) |
| **มี.ค. 2026** | **Trivy / trivy-action** ถูก TeamPCP ยึด: force-push tag 75/76 ตัว + `setup-trivy` + binary v0.69.4 · ต้นเหตุ PAT หลุดจาก `pull_request_target` misconfig · ลาม LiteLLM 1.82.7 / 1.82.8 (PyPI) ผ่าน CI ที่ใช้ Trivy | **tag ของ action = mutable** → pin SHA · ห้าม `pull_request_target` + checkout PR code · credential rotation ต้อง atomic · ปลอดภัย: trivy-action v0.35.0, setup-trivy v0.2.6, trivy v0.69.3 |
| **พ.ค.–มิ.ย. 2026** | PyPI: `durabletask` 1.4.1–1.4.3, `mistralai`, `guardrails-ai` publish ด้วย credential ที่ขโมยมา **โดยไม่ผ่าน GitHub Actions ของโปรเจกต์** · "Hades" 19 package / 37 wheel ฝัง `.pth` startup hook + ข้อความ prompt-injection เล็ง LLM code review | wheel ที่มี `.pth` = flag · release ที่ไม่มี attestation/provenance ตรงกับ CI = flag · ตัว review ที่เป็น LLM ต้องถือ content ใน package เป็น untrusted |
| **ก.ย. 2026** | GitHub Actions `actions-cool/*` ที่ถูกยึดตอน Mini Shai-Hulud **กลับมาออนไลน์พร้อม tag ที่ยังชี้โค้ดร้าย** | workflow ที่ pin SHA ของ commit ก่อน 2026-05-18 ไม่กระทบ — ยืนยันอีกครั้งว่า **SHA pin + ตรวจว่า SHA นั้นสะอาด** |
| **ต.ค. 2026** | รายงาน LiteLLM 1.107.0 ถูกฝัง malware ซ้ำ (PyPI + Docker Hub) — **แหล่งเดียว ยังไม่ยืนยัน** | ถ้าเจอ `litellm` ให้ mark "ต้องยืนยันกับ GHSA/PyPI advisory" |
| **ธ.ค. 2025 → 2026** | npm เปลี่ยนนโยบาย: **classic token ถูก revoke ถาวร (2025-12-09)** · granular token แบบ write ต้อง 2FA + อายุ ≤ 90 วัน · `npm login` ได้ session 2 ชม. · **Trusted Publishing (OIDC)** เป็นทางหลักสำหรับ CI · npm CLI ≥ 11.10 มี `min-release-age` (cooldown) · pnpm มี `minimumReleaseAge` (หน่วยนาที) · Renovate best-practices ตั้ง cooldown 3 วัน | CI ที่ยังใช้ npm token แบบ classic = finding (ใช้ไม่ได้แล้ว + เสี่ยง) · ไม่มี cooldown = Medium (ทุก wave ข้างบนถูกจับได้ภายใน 1–3 วัน) |

---

## 3. Config ป้องกันที่ remediation ควรเสนอ (working config)

```ini
# .npmrc — cooldown 7 วัน กัน version ที่เพิ่ง publish (npm >= 11.10)
min-release-age=7
ignore-scripts=true          # เปิด lifecycle script เฉพาะ package ที่จำเป็นผ่าน allowlist
```
```yaml
# pnpm-workspace.yaml — หน่วยนาที (3 วัน)
minimumReleaseAge: 4320
```
```yaml
# GitHub Actions — publish ด้วย Trusted Publishing (OIDC) ไม่ใช้ long-lived token
permissions:
  id-token: write
  contents: read
steps:
  - uses: actions/checkout@<commit-sha>   # pin SHA เสมอ + comment version
  - run: npm publish --provenance --access public
```
```text
# pip — pin + hash + index เดียว (กัน dependency confusion)
requirements.txt:  package==x.y.z --hash=sha256:...
install:           pip install --require-hashes --index-url <private-index> -r requirements.txt
```
```dockerfile
# base image: LTS line ที่ยัง support + pin digest + ca-certificates ใหม่
FROM node:24-alpine@sha256:<digest>
RUN apk add --no-cache ca-certificates && update-ca-certificates
```

---

## 4. Severity mapping เมื่อเทียบกับ digest

| สิ่งที่พบ | Severity |
|---|---|
| runtime/framework ต่ำกว่า patched **และ** มี Critical RCE ที่ unauthenticated (Node Brotli, Next.js `use cache` / Image / ImageResponse, PostgreSQL 8.8 RCE ที่ exposed) | **Critical** |
| runtime **EOL** (Node 20, Python ≤3.10, PostgreSQL ≤13 / 14 หลัง 2026-11-12, OpenSSL 3.0 / 1.1.1) · Docker Engine < 29.3.1 · Starlette < 1.3.1 ที่รับ form จาก internet | **High** |
| ต่ำกว่า patched แต่ CVE เป็น Medium/Low หรือเงื่อนไข exploit แคบ (เช่น Windows-only, dev-server-only) | **Medium** |
| ไม่มี cooldown / ไม่ใช้ Trusted Publishing / action pin tag แทน SHA | **Medium** (High ถ้า workflow มีสิทธิ์ publish หรือถือ secret prod) |
| CA bundle เก่ากว่า 2026-10-17 ใน image ที่คุย TLS กับภายนอก | **Medium** |

---

## 5. แหล่ง official ที่ใช้สรุป (เช็คซ้ำที่นี่ก่อนฟันธง)

- Node.js: nodejs.org/en/blog/vulnerability/october-2026-security-releases · github.com/nodejs/Release (schedule)
- Next.js: nextjs.org/blog (security releases) · github.com/vercel/next.js/security/advisories
- Python: devguide.python.org/versions · python.org/downloads
- Starlette / FastAPI: github.com/Kludex/starlette/security/advisories · fastapi.tiangolo.com/release-notes
- PostgreSQL: postgresql.org/support/security · postgresql.org/support/versioning
- Docker: docs.docker.com/engine/release-notes/29 · docs.docker.com/security/security-announcements
- OpenSSL: openssl-library.org/news/vulnerabilities · openssl-library.org/policies/releasestrat
- OWASP: owasp.org/Top10/2025 · genai.owasp.org (LLM Top 10:2026 เผยแพร่ 2026-08-04)
- Supply chain: github.blog/changelog (npm) · docs.npmjs.com (trusted publishing) · รายงานของ Elastic / Microsoft / StepSecurity / Snyk สำหรับ Shai-Hulud, Trivy, actions-cool (secondary — ใช้ประกอบ)
