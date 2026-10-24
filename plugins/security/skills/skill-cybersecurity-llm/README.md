# skill-cybersecurity-llm

## Overview
Skill สแกนความปลอดภัยของแอปที่ใช้ LLM/GenAI (chatbot, agent, RAG, tool-calling, MCP) ตาม **OWASP Top 10 for LLM Applications:2026** (+ Agentic Top 10 สำหรับ multi-step agent) — หาช่องโหว่เฉพาะของระบบ AI ที่ SAST ทั่วไปจับไม่ได้ (prompt injection, excessive agency, improper output handling ฯลฯ) สรุปเป็น report จัดระดับ + วิธี mitigate

## วิธีการคิดและการทำงานของ Skill
1. **Discovery** — หาการเรียก LLM SDK/API, prompt, RAG/vector, tool/agent, จุดที่ output ถูกใช้ต่อ
2. **Scan** — ตรวจ LLM01–LLM10:2026 (Prompt Injection, Sensitive Info Disclosure, Excessive Agency, Supply Chain, Data/Model Poisoning, Unbounded Consumption, Misinformation, Hidden Context Exposure, Vector/Embedding, Improper Output Handling)
3. **Score & Report** — จัดระดับ (เน้น output→exec และ agency เกิน) + deep-dive + executive summary

## ผลลัพธ์ที่ได้จากการใช้งาน
- ตาราง finding เฉพาะความเสี่ยง AI/LLM เรียงความรุนแรง
- วิเคราะห์ + แนวทาง mitigate (guardrail, least-privilege tool, output sanitization)
- สรุป posture ของ AI stack

## วิธีใช้
```
/skill-cybersecurity-llm
/skill-cybersecurity-llm src/agent/
/skill-cybersecurity-llm src/rag/
```

## ตัวอย่าง
```
/skill-cybersecurity-llm src/
→ จับ LLM output ที่ถูก exec ตรง ๆ + agent tool ที่สิทธิ์เกิน พร้อมวิธีแก้
```
