---
name: skill-init
description: Create a new Claude Code skill. Use when user asks to create a skill, build a new skill, or says "สร้าง skill". Takes the skill name and purpose as arguments. Generates a complete SKILL.md and supporting file structure.
argument-hint: "[skill-name] [description]"
disable-model-invocation: false
---

# skill-init — Skill Creator

You are creating a new Claude Code skill. Follow the structure and rules below precisely.

## Skill to Create

Name: `$ARGUMENTS[0]`
Purpose: `$ARGUMENTS[1]`

---

## Step 1: Determine Scope

Ask yourself (or the user if unclear):
- **Personal** (`~/.claude/skills/<name>/`) — available in all projects
- **Project** (`.claude/skills/<name>/`) — only this project

Default to **project scope** unless the user says "personal" or "global".

---

## Step 2: Create Directory Structure

```
<scope>/skills/<skill-name>/
├── SKILL.md              ← required entrypoint
├── reference.md          ← (optional) detailed reference material
├── examples/
│   └── example.md        ← (optional) example output
└── scripts/
    └── helper.sh         ← (optional) scripts Claude can run
```

Only create `SKILL.md` unless supporting files are clearly needed.

---

## Step 3: Write SKILL.md

Use this template and fill in based on the skill's purpose:

```markdown
---
name: <skill-name>
description: <Clear description under 250 chars. Include: what it does, when to use it, and trigger phrases.>
argument-hint: <[arg1] [arg2]>   # only if skill takes arguments
disable-model-invocation: <true|false>   # true = user-only (/deploy, /commit)
user-invocable: <true|false>             # false = Claude-only background knowledge
allowed-tools: <Read, Write, Bash, Grep, Glob>   # only tools this skill needs
context: fork    # only if skill should run isolated as a subagent
agent: Explore   # only if context: fork — pick: Explore, Plan, general-purpose
---

# <Skill Title>

<One paragraph explaining what this skill does.>

## Instructions

<Step-by-step instructions for Claude to follow.>
```

---

## Step 4: Choose Invocation Type

| Use Case | Frontmatter |
|---|---|
| User triggers manually (deploy, commit, release) | `disable-model-invocation: true` |
| Claude uses as background knowledge | `user-invocable: false` |
| Both user and Claude can invoke | _(omit both)_ |
| Isolated subagent task | `context: fork` |

---

## Step 5: Use Argument Substitutions If Needed

| Variable | Meaning |
|---|---|
| `$ARGUMENTS` | All arguments as a string |
| `$ARGUMENTS[0]` / `$0` | First argument |
| `$ARGUMENTS[1]` / `$1` | Second argument |
| `${CLAUDE_SKILL_DIR}` | Directory of this skill |
| `${CLAUDE_SESSION_ID}` | Current session ID |

---

## Step 6: Use Dynamic Context If Needed

Use `` !\`command\` `` to inject live shell output into the skill before Claude sees it:

```markdown
## Current git status
!\`git status\`

## Recent commits
!\`git log --oneline -10\`
```

> ⚠️ ตัวอย่างในไฟล์นี้ escape ด้วย `\` เพื่อกันระบบ execute คำสั่งจริงตอนโหลด skill-init — **ตอนเขียนลง skill จริงไม่ต้องใส่ `\`** (เขียน `!` ติด backtick ตรง ๆ)

---

## Step 7: Create the Skill

1. Run `mkdir -p <path>/skills/<skill-name>`
2. Write the `SKILL.md` file at `<path>/skills/<skill-name>/SKILL.md`
3. Write the `README.md` file at `<path>/skills/<skill-name>/README.md` (see Step 8)
4. Create any other supporting files in subdirectories
5. Confirm the skill is ready and show the user both file paths

---

## Step 8: Write README.md (Required)

Every skill **must** include a `README.md` alongside `SKILL.md`. Use this template:

```markdown
# <Skill Name>

## Overview
<อธิบายว่า skill นี้คืออะไร ทำหน้าที่อะไรในโปรเจกต์ เขียน 2-4 ประโยค>

## วิธีการคิดและการทำงานของ Skill
<อธิบาย logic การทำงานภายใน เช่น:
- Skill นี้คิดและตัดสินใจอะไรบ้าง
- ลำดับขั้นตอนที่ skill ทำ
- เงื่อนไขหรือ branch ที่สำคัญ>

## ผลลัพธ์ที่ได้จากการใช้งาน
<อธิบายว่าหลังจากใช้ skill นี้แล้ว ผู้ใช้จะได้อะไรเพิ่มขึ้น เช่น:
- ไฟล์ที่ถูกสร้างหรือแก้ไข
- ความรู้หรือ output ที่ได้รับ
- สิ่งที่เปลี่ยนแปลงในโปรเจกต์>

## วิธีใช้
\`\`\`
/<skill-name> [arguments]
\`\`\`

## ตัวอย่าง
\`\`\`
/<skill-name> example-argument
\`\`\`
```

---

## Rules

- Keep `SKILL.md` under 500 lines; move detail to `reference.md`
- Description must be under 250 characters
- Name: lowercase, hyphens only, max 64 characters (use underscore only if user specifically requests it)
- Do NOT create files the skill does not need
- **Always create both `SKILL.md` and `README.md` — README is mandatory, not optional**
- Always show the user the final `SKILL.md` content after creating it
- If the user asks to create multiple skills, create them one by one and confirm each

---

## Example: Minimal Skill

```markdown
---
name: explain-code
description: Explains code with analogies and ASCII diagrams. Use when asked "how does this work?" or explaining a codebase to someone.
---

When explaining code:
1. Start with a real-world analogy
2. Draw an ASCII diagram of the flow
3. Walk through step by step
4. Highlight one common gotcha
```

## Example: User-Only Task Skill

```markdown
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $0 environment:
1. Run tests — stop if any fail
2. Build the application
3. Push to $0 deployment target
4. Verify deployment health check passes
```

## Example: Skill with Dynamic Context

```markdown
---
name: pr-summary
description: Summarize the current pull request for review
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## PR Context
Diff: !\`gh pr diff\`
Comments: !\`gh pr view --comments\`
Files changed: !\`gh pr diff --name-only\`

Summarize what this PR does, what risks it carries, and whether it's ready to merge.
```
