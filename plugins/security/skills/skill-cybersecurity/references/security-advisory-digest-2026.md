# Security Advisory Digest — 2026 (ข้อมูล ณ 2026-11-25)

สรุป advisory จาก **แหล่ง official** ของ stack ที่องค์กรใช้ (ดู `skill-architecture-standard`) เพื่อให้ทุก skill-cybersecurity* และ subagent-cybersecurity-auditor ใช้ **เทียบ version ที่ detect ได้ → ชี้ finding** ได้ทันทีโดยไม่ต้องเดา

> **วิธีใช้:** detect version จริงจาก lockfile / `Dockerfile` / `.nvmrc` / `pyproject.toml` / `node -v` / `pg_config --version` → เทียบกับคอลัมน์ **patched** และ **EOL** ด้านล่าง → ต่ำกว่า patched = finding (severity ตาม §4) · runtime ที่ EOL = finding **High** เสมอ
> **อายุข้อมูล:** ไฟล์นี้ต้อง refresh **เดือนละครั้ง** หรือเมื่อมี advisory Critical/High ใหม่ · ถ้าวันที่หัวไฟล์เก่ากว่า 45 วัน ให้ mark ใน report ว่า "digest อาจไม่ครบ — ยืนยันกับ advisory DB (GHSA/OSV/NVD)"
> **ไฟล์อื่นห้าม hardcode เลข patched** — ให้อ้าง "patched ตาม digest" เพื่อให้ refresh ที่ไฟล์นี้ไฟล์เดียว

---

## 0. เปลี่ยนอะไรรอบนี้ (2026-10-24 → 2026-11-25)

- **Node.js** security release 2026-11-11 แก้ 16 CVE (High 7) → patched ใหม่ 26.13.1 / 24.22.3 / 22.23.5 · **Node 26 เป็น LTS แล้ว** · Node 25 EOL 2026-06-01
- **Next.js** security release 2026-11-03 แก้ 7 ข้อ (High 1) → 16.4.5 / 15.5.29
- **PostgreSQL** 18.7 / 17.12 / 16.16 / 15.20 · **14 EOL แล้ว** (14.25 เป็นตัวสุดท้าย) · **PostgreSQL 19 GA 2026-11-19**
- **Python** 3.15.2 / 3.14.10 / 3.13.18 / 3.12.16 / 3.11.18 (2026-10-25) — blocklist key ของ eMudhra ใน `ssl`
- **Docker Engine** 29.9.3 (Swarm overlay) และ 29.10.1 (`docker cp` เขียนทะลุ read-only bind mount)
- **OpenSSL** 12 CVE ระดับ Low → 3.5.10 / 4.0.4 / 4.1.1 · **3.6 EOL 2026-11-01**
- **Supply chain:** `agent-framework` (Microsoft, PyPI) 1.26.1–1.26.2 ถูกฝัง stealer (2026-11-17) · **LiteLLM 1.107.0 ยืนยันแล้ว** (MAL-2026-2144)
- **เพิ่มแถว Microsoft Entra ID** เพราะเป็น auth มาตรฐานของทีมแล้ว

---

## 1. Runtime & Framework — patched version / EOL

| Component | Patched (ต่ำกว่านี้ = finding) | EOL / status | ประเด็นสำคัญ 2026 |
|---|---|---|---|
| **Node.js** | **26.13.1** · **24.22.3** · **22.23.5** (2026-11-11) | 20 **EOL 2026-04-30** · 25 **EOL 2026-06-01** · 22 LTS → EOL 2027-04-30 · 24 LTS → EOL 2028-04-30 · **26 LTS ("Lithium") ตั้งแต่ 2026-10-28** → EOL 2029-04-30 · ตั้งแต่ 27 ออกปีละครั้ง ทุกตัวเป็น LTS | **Nov 11 (16 CVE, High 7):** HTTP/2 หลายตัว — remote abort CVE-2026-123863, session cleanup leak CVE-2026-123865, ส่ง memory ที่ free แล้ว CVE-2026-123866, UAF ใน `respondWithFile()` CVE-2026-123874 · HTTPS zero-length write รั่ว heap CVE-2026-123864 · **TLS 1.2 renegotiation เปลี่ยน servername → bypass client-cert auth CVE-2026-123872** · TLS server use-after-destroy CVE-2026-126051 · Medium: `https.Agent` reuse TLS session ข้าม policy → ข้ามการตรวจ cert CVE-2026-123877, proxy credential รั่วใน error CVE-2026-123871 · **Oct 21 (10 CVE):** Brotli decoder RCE CVE-2026-111497, TLS hostname bypass CVE-2026-105483/106069/106072, entropy ซ้ำใน snapshot/SEA CVE-2026-106074 (ต้อง rebuild SEA) |
| **Next.js** | **16.4.5** (Active LTS) · **15.5.29** (Maintenance LTS) (2026-11-03) · ≤14.x ไม่ได้รับ patch | **scheduled security release รายเดือน** (pre-announce บน nextjs.org/blog ~1 สัปดาห์ก่อน) + out-of-band เมื่อ Critical | **Nov 3:** GHSA-mfr8-8qww-v76h **High** `use cache` ที่เรียกทั้งตรงและผ่าน `unstable_cache` → cache ข้าม tenant · Medium: cache key ผิดใน nested `use cache` / binary args (GHSA-vc7v-qv4w-wrv8, GHSA-rhh4-g77r-r9qj), shell cache poisoning แบบ self-hosted, response framing ผิดหลัง reverse proxy ที่ pipeline HTTP/1.1 (GHSA-pc58-hwjq-p385), cookie รั่วผ่าน `x-middleware-set-cookie` ใน Edge route (GHSA-f3mh-rxg3-f5g2), bypass `dangerouslyAllowSVG: false` (GHSA-7qx7-33qx-rqx2) — ส่วนใหญ่กระทบเฉพาะแอปที่เปิด **Cache Components** · **Oct 14:** Critical RCE `use cache` typed arrays (GHSA-673q-mjm6-r5xr) + Image Optimization SVG (CVE-2026-96889, `sharp` ≥ 0.35.5) · Sep 22: Critical RCE `next/og` CVE-2026-94545 · Jul: middleware auth bypass CVE-2026-64642 · Dec 2025: React2Shell CVE-2025-66478 |
| **React** (upstream ของ Next.js) | ตามที่ Next.js patched ดึงมา · ใช้ RSC นอก Next.js: react-server-dom-* **19.0.9 / 19.1.10 / 19.2.9 / 19.3.1** (แหล่งรอง — ยืนยันที่ GHSA-xqc2-xf4c-x3h3) | — | GHSA-xqc2-xf4c-x3h3 **Critical** RCE ใน RSC Flight protocol (typed arrays) · GHSA-h3gv-c5rc-p453 High DoS Server Functions · มี PoC สาธารณะ ยังไม่มีรายงานการโจมตีจริง |
| **Python** | **3.15.2** · **3.14.10** (bugfix) · **3.13.18** · **3.12.16** · **3.11.18** (security-only) (2026-10-25) | **3.10 EOL 2026-10-01** · 3.11 EOL 2027-10 · 3.12 EOL 2028-10 · 3.13 EOL 2029-10 · 3.14 EOL 2030-10 · 3.15 EOL 2031-10 | ต.ค. 2026 ออก 16 release ใน 1 เดือน · ชุด 2026-10-25 **blocklist key ของ eMudhra ใน module `ssl`** (CVE-2026-115557 — แหล่งรอง) ร่วมกับ `certifi` / `pip` / `uv` · ชุด 2026-10-01 แก้ 7 CVE + `tarfile` · binary installer มีเฉพาะ 3.15 / 3.14 |
| **FastAPI / Starlette** | **Starlette ≥ 1.3.1** (ล่าสุด 1.10.0) · FastAPI ล่าสุด 0.165.0 (2026-11-18) | — | ไม่มี advisory ใหม่หลัง 2026-06-12 · ยังต้องเช็ค: CVE-2026-54283 High form DoS (fix 1.3.1), CVE-2026-48818 High StaticFiles UNC/NTLM บน Windows (1.1.0), CVE-2026-48710 "BadHost" path-based auth bypass ใน middleware (1.0.1), CVE-2026-48817 HTTPEndpoint method dispatch · อัปข้ามไป 1.10 มีรายงานว่า routing เปลี่ยน ต้องทดสอบ middleware/API key gate |
| **PostgreSQL** | **18.7** · **17.12** · **16.16** · **15.20** (2026-11-12) · **19.0** (GA 2026-11-19) | **14 EOL แล้ว** (14.25 ตัวสุดท้าย 2026-11-12) · ≤13 EOL · 15 EOL 2027-11-11 | **Nov 12:** release ใหญ่ที่สุดในประวัติ ~52 CVE (นับจากแหล่งรอง; หน้า security official มี ≥ 49 แถว) หลายตัว **CVSS 8.8 รันโค้ดได้** เช่น plpgsql type confusion CVE-2026-120151 และ type confusion CVE-2026-6460 · ยังไม่อยู่ใน CISA KEV · **Aug 13:** 28 CVE (regexp, `to_char`, plperl, refint, pgcrypto เข้ารหัสเป็น cleartext CVE-2026-14663, row security cache CVE-2026-14666) · **PostgreSQL 19:** อย่าใช้ prod จนกว่าจะออก 19.1 (major ใหม่) |
| **Docker Engine / Desktop** | Engine **29.10.1** (2026-11-24) · Desktop **≥ 4.86.0** · Sandboxes ≥ 0.42.0 | — | **29.10.1:** `docker cp` ทำให้ read-only bind mount เขียนได้ CVE-2026-135124 · อ่านไฟล์ user/group mapping ไม่จำกัดขนาด CVE-2026-135844 · **29.10.0 (breaking):** loopback registry ไม่ถือเป็น insecure อัตโนมัติแล้วเมื่อตั้ง `insecure-registries` · **29.9.3:** Swarm overlay เสีย encryption หลัง firewalld flush CVE-2026-115538, worker ได้ cert ของ manager CVE-2026-115539, RSA key CPU CVE-2026-116587 · ก่อนหน้า: AuthZ bypass CVE-2026-34040 (29.3.1), `docker cp` escape CVE-2026-17106 (29.7.0) |
| **OpenSSL** (ใน base image / Python / Node) | **3.5.10** (LTS) · **4.0.4** · **4.1.1** | **3.5 LTS ถึง 2030-04-08** · 4.1 ถึง 2027-11-23 · 4.0 ถึง 2027-05-14 · **3.6 EOL 2026-11-01** · 3.4 / 3.0 / 1.1.1 EOL | **Nov 10 / 17 / 24:** 12 CVE ระดับ **Low** ทั้งหมด (QUIC memory/UAF, AES-GCM-SIV AAD forgery CVE-2026-88823, UAF `PEM_X509_INFO_read_bio_ex` CVE-2026-107493, DANE NULL deref) · **CVE-2026-121481:** CISA ให้ 9.8 แต่ OpenSSL ให้ Low และยังไม่มี fix — ติดตามรอบหน้า · ก่อนหน้า: DTLS High CVE-2026-84782 (3.5.9) |
| **CA trust store** | `ca-certificates` / `certifi` / Go runtime ที่ออกหลัง 2026-10-17 · Python ≥ 3.14.10 / 3.13.18 | — | **eMudhra: key ของ intermediate CA 8 ใบหลุด** (2026-10-17) — browser block แล้ว แต่ client ที่ไม่ใช่ browser ต้องอัปเอง → rebuild image ทุกตัวที่ build ก่อน 2026-10-17 |
| **Microsoft Entra ID / MSAL** (auth มาตรฐาน) | ฝั่ง cloud Microsoft แก้ให้เอง · Microsoft Authenticator (Android) เวอร์ชันล่าสุด | — | CVE-2026-69836 (CVSS 10, deserialization) และ CVE-2026-62869 (spoofing) **แก้ฝั่ง server แล้ว ลูกค้าไม่ต้องทำอะไร** · CVE-2026-80097 (8.6) MSAL broker ใน Authenticator บน Android ให้แอปอื่นขโมย work token ได้ → บังคับอัป Authenticator ผ่าน MDM · ที่ต้องตรวจในโค้ดของเรา: verify `iss` (tenant) / `aud` / `exp` / signature จาก JWKS, ห้ามรับ token จาก tenant อื่นเมื่อแอปเป็น single-tenant (แหล่งรอง — ยืนยันที่ msrc.microsoft.com) |

---

## 2. Supply-chain incidents 2026 — สิ่งที่ scanner ต้องรู้

| เมื่อไร | เหตุการณ์ | บทเรียน / สิ่งที่ต้องตรวจ |
|---|---|---|
| **พ.ย. 2026** | **`agent-framework` (Microsoft, PyPI) 1.26.1 / 1.26.2** ถูก repack นอก CI ของ Microsoft ฝัง stealer ผ่าน **`.pth` startup hook** (ทำงานทุกครั้งที่ Python เริ่ม) ขโมย Azure / Azure DevOps / GitHub Actions token · ตัวสะอาดล่าสุด 1.26.0 · มีรายงาน Mini Shai-Hulud กลับมาที่ `keyv` / `cacheable` (npm) พร้อม provenance ที่ valid (แหล่งเดียว) | ติดตั้ง 1.26.1–1.26.2 = ถือว่าเครื่องถูกยึด rotate ทุก credential · **provenance ไม่ได้แปลว่าปลอดภัย** ถ้า CI ของเจ้าของถูกยึด → ยังต้องมี cooldown |
| **ต.ค. 2026** | **LiteLLM 1.107.0 ยืนยันแล้ว** (OSV **MAL-2026-2144**): release pipeline ถูกยึด wheel ทั้ง 7 ตัว + Docker image `v1.107.0` / `latest` ฝัง stealer + backdoor อยู่บน PyPI ~103 นาที (2026-10-21) · ตัวสะอาดล่าสุด **1.106.2** · กระทบแม้แอปไม่ได้ list LiteLLM ตรง ๆ (transitive) | ถือว่าเครื่อง/container ที่ติดตั้งถูกยึด rotate credential · Docker tag `latest` ก็โดน → pin digest |
| ก.ย. 2025 → พ.ค. 2026 → ส.ค. 2026 | **Shai-Hulud worm** (npm): original → "2.0" → **Mini Shai-Hulud** (TanStack, AntV, Mistral; เข้าทาง GitHub Actions "pwn request" + cache poisoning + ดึง OIDC token จาก runner) → **CHAINDROP** (`keyv` → 400+ package) · ขโมย npm/GitHub token, SSH key, cloud credential, config ของ AI tool · persistence **ลบ home directory ถ้า rotate ก่อนปิด service** | ลำดับแก้: ปิด persistence → rotate → reinstall · indicator: `postinstall` ใหม่ + `bundle.js` / `setup_bun.js`, workflow ที่ bot เพิ่ม, version ไม่มี git tag คู่กัน |
| **มี.ค. 2026** | **Trivy / trivy-action** ถูกยึด (force-push tag 75/76, binary v0.69.4) ต้นเหตุ PAT หลุดจาก `pull_request_target` · ลาม LiteLLM 1.82.7 / 1.82.8 | pin SHA · ห้าม `pull_request_target` + checkout PR code · ตัวปลอดภัย: trivy-action v0.35.0, setup-trivy v0.2.6, trivy v0.69.3 |
| **พ.ค.–มิ.ย. 2026** | PyPI: `durabletask` 1.4.1–1.4.3, `mistralai`, `guardrails-ai` publish ด้วย credential ที่ขโมยมา · "Hades" 37 wheel ฝัง `.pth` + prompt injection เล็ง LLM reviewer | wheel ที่มี `.pth` = flag (เป็น pattern ซ้ำใน agent-framework และ LiteLLM ด้วย) · LLM reviewer ต้องถือ content ใน package เป็น untrusted |
| **ก.ย. 2026** | `actions-cool/*` ที่ถูกยึดกลับมาออนไลน์พร้อม tag ที่ยังชี้โค้ดร้าย | SHA pin + ตรวจว่า SHA นั้นสะอาด (ก่อน 2026-05-18) |
| ธ.ค. 2025 → 2026 | npm: classic token revoke ถาวร · granular write ต้อง 2FA + ≤ 90 วัน · **Trusted Publishing (OIDC)** · npm ≥ 11.10 `min-release-age` · pnpm `minimumReleaseAge` | ยังใช้ classic token = finding · ไม่มี cooldown = Medium |

**Pattern ร่วมของปี 2026:** PyPI ถูกโจมตีด้วย **`.pth` startup hook** 3 ครั้ง (Hades, LiteLLM, agent-framework) และทุกเคสถูกถอนภายใน 2 ชั่วโมงถึง 3 วัน → **cooldown 3–7 วันกันได้เกือบทั้งหมด** · package สาย **AI/agent SDK** เป็นเป้าหลักเพราะเครื่องที่ติดตั้งถือ cloud + AI credential

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
```toml
# uv (pyproject.toml) — cooldown ฝั่ง Python: ไม่รับ release ที่ publish หลัง timestamp นี้
# ให้ CI/Renovate เลื่อนวันที่ให้ช้ากว่าวันนี้ 7 วันเสมอ (เช็ครูปแบบ relative duration ใน docs ของ uv รุ่นที่ใช้)
[tool.uv]
exclude-newer = "2026-11-18T00:00:00Z"
```
```bash
# หา .pth ที่น่าสงสัยใน environment (ของปกติมีแค่ distutils-precedence / editable install)
python -c "import site,glob;[print(p) for d in site.getsitepackages() for p in glob.glob(d+'/*.pth')]"
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
FROM node:26-alpine@sha256:<digest>
RUN apk add --no-cache ca-certificates && update-ca-certificates
```

---

## 4. Severity mapping เมื่อเทียบกับ digest

| สิ่งที่พบ | Severity |
|---|---|
| runtime/framework ต่ำกว่า patched **และ** มี Critical RCE ที่ unauthenticated (Node Brotli, Next.js / React `use cache` + RSC typed arrays, Image Optimization, `next/og`, PostgreSQL 8.8 RCE ที่ exposed) · ติดตั้ง package ที่อยู่ใน §2 ช่วงที่ถูก compromise | **Critical** |
| runtime **EOL** (Node 20 / 25, Python ≤3.10, **PostgreSQL ≤14**, OpenSSL 3.0 / 3.4 / **3.6** / 1.1.1) · Docker Engine < 29.3.1 · Starlette < 1.3.1 ที่รับ form จาก internet · Node ต่ำกว่า patched ที่ใช้ HTTP/2 หรือ TLS client-cert auth · Next.js ต่ำกว่า 16.4.5 ที่เปิด Cache Components แบบ multi-tenant | **High** |
| ต่ำกว่า patched แต่ CVE เป็น Medium/Low หรือเงื่อนไข exploit แคบ (Windows-only, dev-server-only, QUIC ที่ไม่ได้เปิดใช้) | **Medium** |
| ไม่มี cooldown / ไม่ใช้ Trusted Publishing / action pin tag แทน SHA | **Medium** (High ถ้า workflow มีสิทธิ์ publish หรือถือ secret prod) |
| CA bundle เก่ากว่า 2026-10-17 ใน image ที่คุย TLS กับภายนอก · JWT ของ Entra ไม่ตรวจ `iss` / `aud` | **Medium** (High สำหรับ `aud`/`iss` ที่ไม่ตรวจเลย) |
| ใช้ PostgreSQL 19.0 ใน prod (major ใหม่ ยังไม่มี patch release) | **Low** (แนะนำรอ 19.1) |

---

## 5. แหล่ง official ที่ใช้สรุป (เช็คซ้ำที่นี่ก่อนฟันธง)

- Node.js: nodejs.org/en/blog/vulnerability/november-2026-security-releases · nodejs.org/en/about/previous-releases · github.com/nodejs/Release
- Next.js: nextjs.org/blog/november-2026-security-release · github.com/vercel/next.js/security/advisories
- React: github.com/facebook/react/security/advisories
- Python: devguide.python.org/versions · python.org/downloads
- Starlette / FastAPI: github.com/Kludex/starlette/security/advisories · pypi.org/project/starlette · pypi.org/project/fastapi
- PostgreSQL: postgresql.org/support/security · postgresql.org/support/versioning
- Docker: docs.docker.com/engine/release-notes/29 · docs.docker.com/security/security-announcements
- OpenSSL: openssl-library.org/news/vulnerabilities · openssl-library.org/policies/releasestrat
- Microsoft: msrc.microsoft.com/update-guide (Entra ID / Authenticator)
- Malicious packages: osv.dev (MAL-2026-2144 LiteLLM) · รายงานของ Orca / Elastic / JFrog (agent-framework), Mend / StepSecurity (LiteLLM) — secondary ใช้ประกอบ
- OWASP: owasp.org/Top10/2025 · genai.owasp.org (LLM Top 10:2026)
- CISA KEV: cisa.gov/known-exploited-vulnerabilities-catalog (พ.ย. 2026 ยังไม่มีรายการที่ตรงกับ stack ของทีม)
