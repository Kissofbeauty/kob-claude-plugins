# skill-supply-chain

## Overview
Skill สำหรับทำ software supply chain security assessment แบบครอบคลุม **(stack-agnostic — รองรับ npm / pip / go / maven / composer / gem / cargo / nuget)** เมื่อถูกเรียกใช้จะ detect ecosystem ของ project แล้วสำรวจ manifest, lockfile, dependency tree, install scripts และ CI/CD config เพื่อหาความเสี่ยงด้าน supply chain — known CVE, typosquatting, dependency confusion, unpinned versions, malicious install scripts, และ CI/CD ที่ไม่ pin — จากนั้นสรุปเป็น SBOM + report เรียงตาม severity พร้อม remediation roadmap ที่ใช้ได้จริง

## วิธีการคิดและการทำงานของ Skill

1. **Discovery** — detect ecosystem ทั้งหมดใน repo หา manifest + lockfile + CI/CD surface
2. **Dependency Tree** — แยก direct ออกจาก transitive, นับ depth, mark source นอกมาตรฐาน
3. **Known CVE** — เทียบ version ที่ pin จริงกับ known-vulnerable ranges (conservative)
4. **Typosquatting & Dependency Confusion** — ชื่อ package ที่คล้าย/ชนกับ internal
5. **Pinning & Integrity** — หา unpinned ranges, lockfile ครบไหม, hash check
6. **Malicious Install Scripts** — `postinstall`/`setup.py`/`curl|bash` ใน build
7. **CI/CD Supply Chain** — actions ที่ pin ด้วย tag แทน SHA, base image ไม่ pin digest
8. **SBOM + Report** — ตาราง component + findings เรียง severity + remediation roadmap

## ผลลัพธ์ที่ได้จากการใช้งาน
- SBOM ตาราง component (name · version · ecosystem · direct/transitive · hash · license)
- ตาราง findings เรียง severity พร้อม location (ไฟล์:บรรทัด) + evidence
- Remediation roadmap ระบุ priority พร้อม working config (pinned version/SHA จริง)

## วิธีใช้
```
/skill-supply-chain
/skill-supply-chain package.json
/skill-supply-chain .
```

## ตัวอย่าง
```
/skill-supply-chain
→ Detect ทุก ecosystem ใน project, scan dependency + CI/CD, สร้าง SBOM + report เต็ม

/skill-supply-chain package.json
→ โฟกัส manifest เดียว: เช็ค pinning, install scripts, typosquatting, known CVE
```
