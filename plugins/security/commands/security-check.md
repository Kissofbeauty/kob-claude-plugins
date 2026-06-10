---
description: รัน full security audit ของโปรเจกต์ผ่าน subagent-cybersecurity-auditor — auto-scope ครอบ code/API/LLM/supply-chain/secret/container-IaC/threat-model แล้วสรุปเป็น report จัดระดับความรุนแรง + วิธีแก้
argument-hint: "[path] (ว่าง = ทั้ง project)"
---

ผู้ใช้สั่ง `/security-check` เพื่อทำ **full security assessment** ของโปรเจกต์

**Target ที่จะตรวจ:** $ARGUMENTS
(ถ้าว่าง → ตรวจทั้ง project ใน working directory ปัจจุบัน)

## สิ่งที่ต้องทำ
1. **Spawn subagent `subagent-cybersecurity-auditor`** (ผ่าน Agent/Task tool — `subagent_type: subagent-cybersecurity-auditor`) เพื่อรัน security audit บน target ข้างต้น
2. สั่งให้ auditor ทำงานตามที่เซตไว้:
   - **auto-detect scope** — ดูว่าโปรเจกต์มีอะไร (code/API/LLM/dependencies/secrets/Docker-K8s-Terraform/design docs) แล้ว **รันเฉพาะด้านที่เกี่ยว** + log ว่าข้ามด้านไหนเพราะอะไร
   - รวม finding ทุกด้าน → จัดระดับ severity เดียวกัน → report: พลาดตรงไหน (`file:line`) + ทำไม + วิธีแก้ + executive summary/roadmap
   - **defensive-only**, mask secret, อ้าง file:line จริง
3. **แสดง report ที่ subagent ส่งกลับ** ให้ผู้ใช้ครบถ้วน (ranked findings + deep dive + summary)

> หมายเหตุ: งานสแกนหนักให้อยู่ใน subagent เพื่อไม่ให้ context หลัก รก — main agent หน้าที่ spawn + นำเสนอผลเท่านั้น
