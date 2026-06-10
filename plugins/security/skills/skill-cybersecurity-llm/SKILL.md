---
name: skill-cybersecurity-llm
description: LLM/GenAI application security scanner following OWASP Top 10 for LLM Applications:2025. Use when user asks to "ตรวจ LLM security", "scan AI app", "ตรวจ prompt injection", "OWASP LLM", "ตรวจ agent/RAG", "AI security review", or "/skill-cybersecurity-llm".
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# skill-cybersecurity-llm — LLM/GenAI Security Scanner (OWASP LLM Top 10:2025)

สแกนแอปที่ใช้ LLM/GenAI (chatbot, agent, RAG, tool-calling) ตาม **OWASP Top 10 for LLM Applications:2025** แล้วสรุปเป็น report — **ทำครบทุก Phase**

> **Defensive เท่านั้น** — ชี้ช่องโหว่ + วิธี mitigate ไม่เขียน jailbreak/attack พร้อมใช้

---

## Phase 1: Discovery — หา LLM surface
1. หาการเรียก LLM: SDK/API (`openai`, `anthropic`, `@anthropic-ai`, `langchain`, `llamaindex`, `genai`, bedrock), prompt templates, system prompts
2. หา component: RAG/vector store (embeddings, retrieval), tool/function calling, agent loop, MCP, output ที่ถูกเอาไปใช้ต่อ (exec/SQL/HTML/downstream)
3. หาจุดรับ input จากผู้ใช้/ภายนอกที่ไหลเข้า prompt

## Phase 2: Scan — OWASP LLM Top 10:2025
ตรวจครบ **LLM01–LLM10** ตาม pattern ใน **`references/llm-top10-2025.md`**:
- LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Supply Chain · LLM04 Data & Model Poisoning · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM08 Vector & Embedding Weaknesses · LLM09 Misinformation · LLM10 Unbounded Consumption

## Phase 3–5: Score → Deep-dive → Report
- ให้คะแนน severity (เน้น: input ภายนอกไหลเข้า prompt, output ไป exec/SQL/HTML, agent มีสิทธิ์ทำ action จริง)
- ตาราง ranked findings → deep-dive (Root Cause / Attack Scenario / Vulnerable Code / Remediation) → executive summary
- ใช้เกณฑ์/เทมเพลตเดียวกับ `skill-cybersecurity` (`references/scoring-and-report.md`)

---

## Rules
- ทำครบทุก Phase · ไม่พบในหมวดใดให้ระบุ "✅ No issues found" + บอกว่าตรวจอะไร
- อ้าง **file:line จริง** · remediation เป็น working code/pattern
- จุดเสี่ยงสูงสุดมัก: **LLM05 Improper Output Handling** (output → exec/SQL/XSS) + **LLM06 Excessive Agency** (agent/tool มีสิทธิ์เกิน) — เน้นตรวจ
- conservative scoring · **defensive-only** (อธิบายความเสี่ยง ไม่ให้ payload โจมตีพร้อมใช้)

## References
| ไฟล์ | เนื้อหา |
|---|---|
| `references/llm-top10-2025.md` | LLM01–LLM10:2025 + pattern + วิธี mitigate |
