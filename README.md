# kissofbeauty — Kiss of Beauty Marketplace

Kiss of Beauty's **Claude plugin marketplace**, maintained by the **BI Team**.
A single home for the org's plugins, skills, subagents, and working standards — install once, use in every project, and receive updates continuously.

- **Marketplace:** `kissofbeauty`
- **Owner:** BI-Team · database@kissofbeauty.co.th

---

## 📦 Plugins

| Plugin | What it covers | Skills / Agents |
|---|---|---|
| [`management`](plugins/management) | PM & orchestration | `skill-PM` (discovery → Project Proposal → build-ladder orchestration) · `precompact` (save PM state to `docs/pm-handoff.md` before compact) · `skill-init` (scaffold new skills) |
| [`devops`](plugins/devops) | Engineering standards | `skill-git-standard` (Git/GitHub: main←uat←feature, credential gate, PR-only) · `skill-docker-standard` (containerization) · `skill-architecture-standard` (approved stack + UAT/prod topology) |
| [`security`](plugins/security) | Security toolkit | `skill-cybersecurity` (OWASP code scan) · `-api` (API Top 10:2023) · `-llm` (LLM Top 10:2025) · `-supply-chain` (SCA/deps) · `-secret-scan` (secrets + git history) · `-container-iac` (Docker/K8s/Terraform) · `-threat-model` (STRIDE) · **subagent** `subagent-cybersecurity-auditor` (full audit) · **command** `/security-check [path]` |
| [`developer`](plugins/developer) | Engineering team | `skill-frontend-web` · `skill-backend` · `skill-sql` · `skill-data-modeling` (UUID v7 / soft-delete / hand-written SQL migrations) · `skill-erd-dbml` (ERD docs for dbdiagram.io) · `skill-python` (venv-per-project) · `skill-fastapi` · `ui-ux-pro-max` (design intelligence) · `skill-software-testing` (test + UAT) · **subagents** `subagent-data-architect` (schema design, PM-gated) + `subagent-fullstack` (build per proposal) + `subagent-qa-tester` (test/UAT/security + PM-mediated fix loop) |

---

## 🗺️ Skill Map & Team Workflow

The marketplace has 4 plugins by role — **management** (plan) · **devops** (engineering standards) · **security** (safety) · **developer** (hands-on build).

### Full skill map

```
kob-claude-plugins  (marketplace: kissofbeauty)
│
├── management ──┬── skill-PM ──────────────── main agent = PM: user talks → 📄 Project Proposal
│   (planning)   │                            → orchestration ladder (features → stack → design → data → build → test)
│                ├── precompact ────────────── save PM state to docs/pm-handoff.md before compact (seamless resume)
│                └── skill-init ───────────── scaffold a new skill (SKILL.md + README) to standard
│
├── devops ──────┬── skill-git-standard ───── git standard: main←uat←feature, credential gate, PR-only
│   (standards)  ├── skill-docker-standard ── containerize: dev via compose, no creds in images,
│                │                            BI builds from main → private registry
│                └── skill-architecture-standard ── approved stack/tools + UAT/prod topology
│
├── security ────┬── skill-cybersecurity ──────────── code scan, OWASP Top 10:2025
│   (safety)     ├── skill-cybersecurity-api ───────── OWASP API Top 10:2023
│                ├── skill-cybersecurity-llm ───────── OWASP LLM Top 10:2025
│                ├── skill-cybersecurity-supply-chain ─ SCA / deps / CVE
│                ├── skill-cybersecurity-secret-scan ── secrets + git history
│                ├── skill-cybersecurity-container-iac ─ Docker/K8s/Terraform
│                ├── skill-cybersecurity-threat-model ─ STRIDE (design-level)
│                ├── 🤖 subagent-cybersecurity-auditor ─ all dimensions → one report
│                └── ⌘ /security-check ──────────────── audit the whole project
│
└── developer ───┬── skill-frontend-web ────── HTML/CSS/SCSS/Tailwind/JS/TS/React
    (dev team)   ├── skill-backend ─────────── API/server design + controller/service/repository
                 ├── skill-sql ─────────────── schema/query/security/migration (hand-written SQL)
                 ├── skill-data-modeling ───── team data-model standard: UUID v7 PK, soft-delete,
                 │                            new-table-vs-extend criteria, S3 for files
                 ├── skill-erd-dbml ────────── docs/erd.dbml + docs/erd-readme.md (dbdiagram.io)
                 ├── skill-python ──────────── PEP8/OOP/SOLID + venv per project
                 ├── skill-fastapi ─────────── FastAPI (data API / ML serving)
                 ├── ui-ux-pro-max ─────────── design intelligence → docs/brief-design.md → Claude Design
                 ├── skill-software-testing ── test design + UAT + defect reports
                 ├── 🤖 subagent-data-architect ─ schema design → docs/data-model.md + ERD (PM-gated)
                 ├── 🤖 subagent-fullstack ─── build per proposal, backend-first (uses all coding skills)
                 └── 🤖 subagent-qa-tester ─── test + UAT + security → fix loop via PM
```

### Build workflow (orchestration ladder — `skill-PM` §2.5)

```
🧑 user ↔ skill-PM ──► 1. 📄 docs/project-proposal.md (approved)
                       2. 📄 docs/features.md      (modules/features agreed with user)
                       3. 📄 docs/stack.md         (user-defined or architecture standard;
                          │                         fixed: PostgreSQL + docker compose)
                       4. ui-ux-pro-max ──► 📄 docs/brief-design.md
                          │        └─► 🧑 user pastes into Claude Design ──► source code
                          │             (one-page interactive app = the project's design system)
                       5. 🤖 subagent-data-architect ──► 📄 docs/data-model.md
                          │                              + docs/erd.dbml + docs/erd-readme.md
                       6. 🚧 gate: PM approves schema
                       7. 🤖 subagent-fullstack — backend first (.sql + API from data-model.md),
                          │                       then frontend on top of the Claude Design code
                       8. 🤖 subagent-qa-tester + user test on dev stage → defect loop until clean
                       9. 🚀 hosting/production deploy = BI team (human) — agents never deploy prod
```

**Reading the flow:**
1. **PM** (`skill-PM`) talks to the user and distills a **Project Proposal** (the outcome doesn't have to be an app — if nothing needs building, it ends here).
2. For web/webapp work PM walks the ladder **in order, no skipping**: features → stack → design brief.
3. **ui-ux-pro-max** writes `docs/brief-design.md`; the user feeds it to **Claude Design** (external) and brings back the source code — this code **is** the design system; builders extend it, never rewrite it.
4. Anything touching the data model goes through **subagent-data-architect only** → `docs/data-model.md` + ERD docs (`erd.dbml` + `erd-readme.md` always updated together). PM gates the schema.
5. **subagent-fullstack** builds backend first from `data-model.md`, then the frontend on top of the design code; **subagent-qa-tester** and the user verify on dev stage; the **BI team** takes it to hosting.

> Every stage follows the standards: git (`skill-git-standard`) · containers (`skill-docker-standard`) · stack (`skill-architecture-standard`) · security gate before deploy.

---

## 🚀 How to Install (per surface)

Skills are distributed through **2 channels**, because Claude Code and claude.ai use different mechanisms:

### A) Claude Code (pulls straight from this repo)

> ✅ **This repo is public** — anyone can `marketplace add` and install without being an org member (Claude Code pulls via git).
> (**Write** access is still limited to collaborators/org — see `CONTRIBUTING.md`.)

```bash
# 1. Add the marketplace — either form works:
/plugin marketplace add Kissofbeauty/kob-claude-plugins              # owner/repo
/plugin marketplace add https://github.com/Kissofbeauty/kob-claude-plugins.git   # full git URL

# 2. Install a plugin
/plugin install devops@kissofbeauty
```

- After installing, e.g. `skill-git-standard` is picked up automatically for git work, or invoke directly: `/devops:skill-git-standard`
- **Update:** `/plugin marketplace update kissofbeauty` (pulls the latest commit automatically)
- Plugins **don't set a `version`** → every commit on `main` is the latest version

> ❗ **"Repository not found"** = repo name typo, or the repo isn't public (check Settings → Visibility)

### B) claude.ai — chat / cowork / Projects

The same skills work on claude.ai (`SKILL.md` is the same open format), but claude.ai **does not pull from GitHub** — an **admin** must publish them into the workspace:

- Admin uploads/updates skills at **`claude.ai/admin-settings/skills`** → provisioned to every org member automatically
- To target specific groups: bundle skills as a plugin and assign it to a group
- Only available to members of the **Claude for Team workspace** (personal accounts must be invited in first)
- ⚠️ Publishing is currently **manual** — there is no Admin API to automate it yet

> Full details/constraints: see [`requirements.md`](requirements.md) §5.1 (distribution matrix) and §8 (Spike S1)

---

## 🗂️ Repo Structure

```
.
├── .claude-plugin/marketplace.json    # marketplace index
├── plugins/
│   ├── management/                    # skill-PM · precompact · skill-init
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/<skill>/            (SKILL.md + README.md)
│   ├── devops/                        # git / docker / architecture standards
│   ├── security/                      # cybersecurity skills + auditor subagent
│   │   ├── skills/  agents/  commands/
│   └── developer/                     # coding skills + fullstack/qa/data-architect subagents
│       ├── skills/  agents/
├── scripts/validate.py                # manifest/skill validator (run before PRs)
├── .github/workflows/validate.yml     # CI: validate.py on every push/PR
├── CLAUDE.md                          # project context (read before working)
├── requirements.md                    # requirements + scope + decisions
├── CONTRIBUTING.md                    # how BI devs add/change plugins
└── README.md
```

---

## 📚 Technical Information

**Tech stack:** no runtime — this is a content/manifest repo (Markdown + JSON). `marketplace.json` / `plugin.json` follow the Claude Code plugin spec; `SKILL.md` follows the Agent Skills open format (works on both Claude Code and claude.ai).

**Branch model (org standard):** `main` (production/published) ← `uat` ← `feature/<name>` — both `main` and `uat` are protected, PR-only. Conventional Commits. A pre-commit hook validates manifests and scans for credentials.

**Key docs:**

| File | For |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Project context — read before every work session |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | **Devs** adding/changing plugins · branch model · validation · governance |
| [`requirements.md`](requirements.md) | Scope · design decisions · distribution strategy |

**Gotchas:**
- claude.ai does not auto-update from git → skills must be re-published by an admin after merge
- Manifests must always be valid JSON — a broken `marketplace.json`/`plugin.json` breaks the whole marketplace
- Secrets/PII must never enter git — `.gitignore` covers `.env` and secret files; the pre-commit gate enforces it

---

## ➕ Adding a Skill / Plugin

Full steps in **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — in short:
1. Branch `feature/<name>` from `uat`
2. Place files to standard (skill → `plugins/<plugin>/skills/<name>/SKILL.md` + `README.md`)
3. Run `python scripts/validate.py` until it passes
4. Open a PR to `uat` → human review + security gate → merge (then `uat` → `main` to publish)
