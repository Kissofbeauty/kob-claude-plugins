# skill-container-iac

## Overview
Skill สำหรับสแกนหา misconfiguration ด้านความปลอดภัยใน **container image และ Infrastructure-as-Code** เมื่อถูกเรียกใช้จะ detect ประเภทไฟล์ IaC (Dockerfile, docker-compose, Kubernetes manifest, Helm, Terraform) แล้วตรวจตาม checklist ของแต่ละประเภท — รัน as root, `:latest`/ไม่ pin digest, secret ฝังใน image, privileged pod, ไม่ตั้ง resource limits, storage public, security group เปิดกว้าง, IAM กว้างเกิน ฯลฯ — จากนั้นเรียงตาม severity และสรุปเป็น report พร้อม remediation ที่ใช้ได้จริง **(defensive-only)**

## วิธีการคิดและการทำงานของ Skill

1. **Discovery** — สำรวจ target แล้ว detect ว่ามี IaC ประเภทใด (Dockerfile / Compose / k8s / Helm / Terraform)
2. **Dockerfile / Compose checks** — root user, latest tag, secret ใน ENV/ARG, ADD vs COPY, cache/attack surface, privileged
3. **Kubernetes checks** — privileged, hostPath/hostNetwork, resource limits, runAsNonRoot, capabilities, secret plaintext
4. **Terraform / IaC misconfig** — public storage, SG 0.0.0.0/0, unencrypted storage, IAM wildcard, hardcoded secret
5. **Base image / dependency CVE** — ชี้ base image เก่า/ไม่ pin + เสนอ tool เสริม (trivy/hadolint) ถ้ามี
6. **Report** — เรียงตาม severity พร้อม location จริง + remediation ❌→✅

## ผลลัพธ์ที่ได้จากการใช้งาน
- ตาราง finding เรียงตาม severity พร้อมไฟล์ + บรรทัดจริง
- Remediation รายข้อเป็น config ที่ใช้ได้จริง (bad → good)
- สรุป Critical Actions + ลำดับการแก้

## วิธีใช้
```
/skill-container-iac
/skill-container-iac Dockerfile
/skill-container-iac k8s/
/skill-container-iac infra/terraform/
```

## ตัวอย่าง
```
/skill-container-iac
→ Detect IaC ทั้ง project แล้วสแกนครบทุกประเภทที่เจอ + report เรียง severity

/skill-container-iac Dockerfile
→ ตรวจ Dockerfile ไฟล์เดียว: root user, latest tag, secret, ADD/COPY + วิธี harden
```
