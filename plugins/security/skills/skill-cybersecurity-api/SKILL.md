---
name: skill-cybersecurity-api
description: API security scanner following OWASP API Security Top 10:2023. Use when user asks to "ตรวจ API security", "scan API", "API security review", "OWASP API", "ตรวจ REST/GraphQL", "ตรวจ endpoint", or "/skill-cybersecurity-api".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-cybersecurity-api — API Security Scanner (OWASP API Top 10:2023)

สแกน API (REST/GraphQL/gRPC) หาช่องโหว่ตาม **OWASP API Security Top 10:2023** แล้วสรุปเป็น report — **ทำครบทุก Phase**

> **Defensive เท่านั้น** · **Stack-agnostic** — detect framework ก่อนแล้วปรับการตรวจ

---

## Phase 1: Discovery — หา API surface
1. Detect framework + route definitions: Express/Fastify (`app.get/post`), FastAPI/Flask (`@app.route`, `@router`), Spring (`@RequestMapping`), Django REST, GraphQL schema/resolvers, gRPC `.proto`
2. ทำรายการ endpoints + method + auth ที่ผูกอยู่ + input/params
3. หา API docs/spec (OpenAPI/Swagger `*.yaml`, GraphQL schema) เทียบกับ route จริง (หา shadow/undocumented)

## Phase 2: Scan — OWASP API Top 10:2023
ตรวจครบ **API1–API10** ตาม pattern ใน **`references/api-top10-2023.md`** (3 ใน 5 อันดับแรกเป็นเรื่อง authorization — เน้นเป็นพิเศษ):
- API1 BOLA · API2 Broken Authentication · API3 Broken Object Property Level Authz · API4 Unrestricted Resource Consumption · API5 Broken Function Level Authz · API6 Unrestricted Access to Sensitive Business Flows · API7 SSRF · API8 Security Misconfiguration · API9 Improper Inventory Management · API10 Unsafe Consumption of APIs

## Phase 3–5: Score → Deep-dive → Report
- ให้คะแนน severity (Critical/High/Medium/Low/Info) — เน้น exploitability + impact + exposed-to-internet
- ตาราง ranked findings → deep-dive ทุก finding (Root Cause / Attack Scenario / Vulnerable Code / Remediation) → executive summary
- ใช้เกณฑ์/เทมเพลตเดียวกับ `skill-cybersecurity` (`references/scoring-and-report.md` ของ skill นั้น)

---

## Rules
- ทำครบทุก Phase · ไม่พบในหมวดใดให้ระบุ "✅ No issues found" + บอกว่าตรวจอะไร
- อ้าง **endpoint + file:line จริง** · remediation เป็น working code
- เน้น **authorization** (API1/API3/API5) เพราะเป็นช่องโหว่ API ที่พบบ่อยสุด
- conservative scoring · **defensive-only**

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/api-top10-2023.md` | API1–API10:2023 + pattern + ตัวอย่าง bad→good |
