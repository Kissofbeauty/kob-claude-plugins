---
name: skill-container-iac
description: Container & Infrastructure-as-Code security scanner. Use when user asks to "ตรวจ Dockerfile", "ตรวจ k8s", "ตรวจ terraform", "scan container", "container security", "IaC security", "ตรวจ docker-compose", "harden Kubernetes", or "/skill-container-iac".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-container-iac — Container & IaC Security Scanner

เมื่อถูกเรียก ให้สแกนหา misconfiguration ด้านความปลอดภัยใน container image และ Infrastructure-as-Code แล้วสรุปเป็น report — **ทำครบทุก Phase ตามลำดับ**

> **Defensive-only:** ชี้จุดเสี่ยง + วิธีแก้ (hardening) เท่านั้น — ไม่เขียน exploit / ไม่สร้าง config ที่ใช้โจมตี

---

## Phase 1: Discovery — สำรวจ + detect ไฟล์ IaC

1. ผู้ใช้ระบุ path/ไฟล์/โฟลเดอร์ → scan ตามนั้น · ไม่ระบุ → ทั้ง project ใน working directory
2. **Detect ประเภทไฟล์** (ใช้ Glob + Grep) แล้วเลือก check set ตามที่เจอ:

   | ประเภท | ไฟล์บ่งชี้ | check set |
   |---|---|---|
   | Dockerfile | `Dockerfile*`, `Containerfile`, `*.dockerfile` | Phase 2 |
   | Compose | `docker-compose*.yml`, `compose*.yaml` | Phase 2 + 3 |
   | Kubernetes | `*.yaml`/`*.yml` ที่มี `kind:` (Deployment/Pod/Service/…) | Phase 3 |
   | Helm | `Chart.yaml`, `values*.yaml`, `templates/*.yaml` | Phase 3 |
   | Terraform | `*.tf`, `*.tf.json`, `*.tfvars` | Phase 4 |

   > k8s manifest แยกจาก YAML ทั่วไปด้วยการ Grep หา `^kind:` + `apiVersion:`
3. รวมรายการไฟล์ที่จะตรวจ + บอกว่าเจอ IaC ประเภทใดบ้างก่อนเริ่มสแกน

---

## Phase 2: Dockerfile / Compose checks

ตรวจ pattern เต็มใน **`references/container-iac-checks.md` (ส่วน Dockerfile)** อย่างน้อยต้องครอบ:

- รัน **as root** (ไม่มี `USER` non-root) → privilege escalation
- ใช้ base image tag **`:latest`** หรือ **ไม่ pin digest** (`@sha256:`) → non-reproducible / supply chain
- **secret ใน `ENV`/`ARG`** (password, token, key) → รั่วเข้า image layer
- **`ADD`** จาก remote/URL แทน `COPY` → MITM / unexpected fetch
- ติดตั้งของไม่จำเป็น / ไม่ลบ cache (`apt-get` ไม่ `--no-install-recommends`, ไม่ clean) → attack surface โต
- ไม่ `--no-cache` / ทิ้ง package manager metadata
- เปิด port หรือ mount ที่ไม่จำเป็น (compose: `privileged: true`, `network_mode: host`, bind socket `/var/run/docker.sock`)

---

## Phase 3: Kubernetes checks

ตรวจ pattern เต็มใน **`references/container-iac-checks.md` (ส่วน Kubernetes)** อย่างน้อยต้องครอบ:

- `securityContext.privileged: true` → เทียบเท่า root บน host
- `hostNetwork` / `hostPID` / `hostIPC` / `hostPath` volume → ทะลุ namespace isolation
- **ไม่ตั้ง resource `limits`/`requests`** → DoS / noisy neighbor
- **ไม่ตั้ง `runAsNonRoot: true`** / ไม่ตั้ง `readOnlyRootFilesystem` / `allowPrivilegeEscalation` ไม่เป็น false
- `capabilities.add` เกินจำเป็น (เช่น `SYS_ADMIN`, `NET_ADMIN`) / ไม่ `drop: [ALL]`
- **Secret เป็น plaintext** ใน manifest หรือ env `value:` → ควรใช้ `secretKeyRef` / external secret
- image ใช้ `:latest` / `imagePullPolicy` ไม่เหมาะ

---

## Phase 4: Terraform / IaC misconfiguration

ตรวจ pattern เต็มใน **`references/container-iac-checks.md` (ส่วน Terraform)** อย่างน้อยต้องครอบ:

- **Storage public** — S3 `acl = "public-read"`, ไม่มี `block_public_access`, GCS/Blob public
- **Security group / firewall เปิดกว้าง** — `cidr_blocks = ["0.0.0.0/0"]` บน port admin (22/3389/3306/…)
- **Unencrypted storage** — ไม่ตั้ง `encrypted = true` / ไม่มี KMS บน EBS/RDS/S3
- **IAM กว้างเกิน** — `Action = "*"` / `Resource = "*"` / `"Effect": "Allow"` แบบ wildcard
- logging/versioning ปิด, hardcoded secret ใน `.tf`/`.tfvars`

---

## Phase 5: Base image / dependency CVE

- ดึง base image + tag จาก Dockerfile/manifest → ระบุความเสี่ยง version เก่า / EOL / ไม่ pin
- ถ้ามี `trivy`/`hadolint`/`grype` ใน PATH (เช็คด้วย Bash) → เสนอรันเสริม (ไม่บังคับ) — ไม่มีก็วิเคราะห์ด้วย pattern แบบ static
- หา lockfile/manifest ของ dependency ใน image แล้วชี้ component ที่ควร audit

---

## Phase 6: Report

สรุปผลเรียงตาม **severity** (Critical → High → Medium → Low → Info):

- ตาราง summary: ID · ไฟล์:บรรทัด · ประเภท (Dockerfile/k8s/TF) · severity · สรุปสั้น
- แต่ละ finding: **Risk** (เกิดอะไรได้) · **Location** (ไฟล์ + บรรทัดจริง) · **Remediation** (config ที่ใช้ได้จริง ❌→✅)
- ปิดท้าย: Critical Actions + ลำดับการแก้

---

## Rules

- ทำครบทุก Phase ที่เกี่ยวกับไฟล์ที่เจอ · หมวดใดไม่พบให้ระบุ "✅ No issues found" พร้อมบอกว่าตรวจอะไรไป
- อ้าง **ไฟล์ + line number จริง**เสมอ
- remediation ต้องเป็น **config ที่ใช้ได้จริง** ไม่ใช่ pseudo-config
- ให้คะแนนแบบ **อนุรักษ์นิยม**: ไม่แน่ใจระหว่าง High/Medium → เลือก High
- **Defensive เท่านั้น:** ชี้จุดเสี่ยง + วิธี harden — ไม่เขียน exploit พร้อมใช้

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/container-iac-checks.md` | checklist ละเอียด Dockerfile / Kubernetes / Terraform + ตัวอย่าง ❌ bad → ✅ good |
