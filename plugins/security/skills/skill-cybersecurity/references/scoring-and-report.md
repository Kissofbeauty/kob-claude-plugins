# Scoring & Report Templates — skill-cybersecurity

เกณฑ์ให้คะแนน + เทมเพลตผลลัพธ์สำหรับ Phase 3–6 (stack-agnostic — ใช้ได้ทุกภาษา)

---

## Phase 3 — Risk Scoring (CVSS v4.0 ประยุกต์)

| ระดับ | คะแนน | เกณฑ์ |
|---|---|---|
| Critical | 9.0–10.0 | RCE, auth bypass ทั้งหมด, data breach ขนาดใหญ่ |
| High | 7.0–8.9 | Privilege escalation, SQL injection, hardcoded secrets |
| Medium | 4.0–6.9 | IDOR, XSS, weak crypto, misconfiguration |
| Low | 0.1–3.9 | Missing headers, verbose errors, outdated minor dep |
| Info | 0 | Best-practice suggestions, ไม่ใช่ vulnerability โดยตรง |

**พิจารณาจาก:**
- **Exploitability** — ใช้งานง่ายแค่ไหน (network/local, no-auth/auth-required)
- **Impact** — ผลต่อ Confidentiality / Integrity / Availability
- **Context** — exposed ต่อ internet หรือ internal only

---

## Phase 4 — Ranked Finding List

ตาราง summary เรียงคะแนนสูงสุด→ต่ำสุด:

```
| # | Severity | Score | ID       | Title                          | Location              |
|---|----------|-------|----------|--------------------------------|-----------------------|
| 1 | Critical | 9.5   | VULN-001 | SQL Injection in login()       | src/auth/client.py:42 |
| 2 | High     | 8.1   | VULN-002 | Hardcoded secret key           | config.py:5           |
```

---

## Phase 5 — Deep Dive (ทุก finding)

```markdown
### [VULN-XXX] <Title> — <Severity> (<Score>)

**Location:** `file_path:line_number`
**OWASP Category:** A0X:2025 — <Category Name>

#### Root Cause
อธิบายว่าทำไมโค้ดนี้ถึงมีช่องโหว่ — เน้น WHY ไม่ใช่แค่ WHAT

#### Attack Scenario
อธิบาย step-by-step ว่า attacker จะ exploit ยังไง (เชิงอธิบายความเสี่ยง — ไม่ใช่ exploit พร้อมใช้)

#### Vulnerable Code
<โค้ดที่มีปัญหา ตัดมาจากไฟล์จริง พร้อม line number>

#### Remediation
<โค้ดที่แก้ไขแล้ว — working code ในภาษาของ target>

#### Additional Hardening
- แนะนำ library/pattern เพิ่มเติมถ้ามี
```

---

## Phase 6 — Executive Summary Report

```markdown
## Security Assessment Report

**Scanned:** <paths>
**Stack:** <ภาษา/เฟรมเวิร์กที่ detect ได้>
**Date:** <วันที่วันนี้>
**Total Findings:** X (Critical: X | High: X | Medium: X | Low: X | Info: X)

### Risk Overview
[breakdown ของ findings / กราฟ ASCII]

### Critical Actions Required
1. [สิ่งที่ต้องแก้ทันที]

### Remediation Roadmap
| Priority | Action | Effort | Impact |
|---|---|---|---|
| Immediate | Fix VULN-001, VULN-002 | Low | Critical |
| Short-term (1–2 weeks) | Fix VULN-003 to 005 | Medium | High |
| Medium-term (1 month) | Fix VULN-006+ | High | Medium |

### Overall Security Posture
[ประเมินภาพรวม: ระดับ security ปัจจุบันเป็นอย่างไร]
```
