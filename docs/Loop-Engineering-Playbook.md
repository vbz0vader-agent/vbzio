# Loop Engineering Playbook

**Status:** Approved blueprint (Approach A) — v1 power = soft window only  
**Last updated:** 2026-10-06 (AEDT) — Cursor plugins + CLI login auth + Spec Kit + hg61→hg62 deploy (see §12 Changelog)  
**Canonical human copy:** Obsidian `localdev` → Development Structure → Loop  
**Agent copy:** hg61 `~/loop/docs/Loop-Engineering-Playbook.md` (keep in sync)  
**Homelab inventory:** Notion → Technology → Home Servers (not this doc)

When Cursor CLI (Tech Lead **and** Coder) needs process context, **read this file first**.

---

## 1. Goal

Overnight, unattended software delivery loop:

1. Human sets goals and GitHub Issues in a Sprint.
2. **Tech Lead** (Cursor CLI) turns Issues into small specs + Definition of Done.
3. **Coder** (Cursor CLI, separate headless session, default model `composer-2.5`) implements and tests until DoD.
4. Tech Lead reviews; opens a PR for human morning review.

Optimize for **effectiveness** and **economy** (Cursor Pro quota, electricity).

**Stack (since 2026-10-06):** GrokBot (control plane) + Cursor CLI (the only coding agent). All model usage is on Cursor Pro (edc898@gmail.com); GitHub identity stays **vbz0vader-agent**. Pi, OpenHands and OpenAI Codex CLI were removed from hg61; OpenRouter / SiliconFlow are no longer used for coding.

---

## 2. Roles

| Role | Actor | Responsibilities | Out of scope |
|---|---|---|---|
| Product Owner | Human (Eddie) | Priorities, sprint scope, morning PR review/merge, product unblock | Overnight coding |
| Control plane | GrokBot on HPG8 (daytime) | Help write Issues, board hygiene, quotas, lab ops, morning digest | Long unattended code loops |
| Tech Lead | Cursor CLI `agent` on hg61 | Context → break down Issue → `N-spec.md` + DoD → review plan/diff → follow-ups or `gh pr create` | Implementing code in the spec/review session |
| Coder | Cursor CLI `agent` on hg61 (separate `--print` session, `composer-2.5`) | `N-plan.md` → implement/test to DoD → `N-walkthrough.md` | Inventing scope; final PR without Tech Lead |
| Orchestrator | `loopctl` (no LLM) on hg61 | Labels, invoke agents, timeouts, budgets, logging | Thinking / writing product code |

**Agent count:** exactly **1 LLM coding agent (Cursor CLI) in 2 roles** (Tech Lead + Coder) + **1 dumb orchestrator**.  
Pi, OpenHands and Codex CLI were **removed** on 2026-10-06 — no secondary coding agent.

---

## 3. GitHub structure

- **Project** per product (Kanban + **Iteration** = Sprint).
- **Issue** = Story/ticket (types/labels: story, bug, chore).
- **Status idea:** Backlog → Ready → Speccing → Coding → Review → PR Ready → Done.

### Labels (agent contract)

| Label | Meaning |
|---|---|
| `loop:ready` | Human released Issue for Tech Lead |
| `loop:specced` | Spec + DoD written |
| `loop:coding` | Coder (Cursor CLI) working |
| `loop:needs-review` | Walkthrough ready for Tech Lead |
| `loop:changes-requested` | Tech Lead follow-up for the Coder |
| `loop:pr-open` | PR awaiting human |
| `loop:blocked` | Needs human (deadline, ambiguity, failed rounds) |

### Repo artifacts (Issue `#N`)

| File | Author |
|---|---|
| `docs/tasks/N-spec.md` | Tech Lead — requirements + DoD checklist |
| `docs/tasks/N-plan.md` | Coder (Cursor CLI) — implementation plan (Tech Lead may edit before coding) |
| `docs/tasks/N-walkthrough.md` | Coder (Cursor CLI) — what changed, how to verify |

Issue comments = short status. **Files + PR** = source of truth for agents.

**New projects (Spec Kit):** use `specs/NNN-name/{spec,plan,tasks}.md` in place of `docs/tasks/N-spec.md` and `N-plan.md` (see §7 Spec Kit). Existing repos (vbzio) keep `docs/tasks/`.

---

## 4. State machine

```
human: Issue in Sprint + loop:ready
  → loopctl claims → Cursor CLI Tech Lead
  → writes N-spec.md + DoD → loop:specced
  → loopctl starts Coder (Cursor CLI session)
  → Coder writes N-plan.md → (optional Tech Lead plan check)
  → Coder implement/test loop → N-walkthrough.md → loop:needs-review
  → Cursor CLI review (Tech Lead)
       ├─ fail → comment + loop:changes-requested → Coder (max rounds)
       └─ pass → gh pr create → loop:pr-open
  → human morning: review / merge
```

**Concurrency (v1):** 1 Tech Lead session + **1** Coder session (both Cursor CLI). Raise Coder concurrency only after stable and only if the Cursor Models pool has headroom.

---

## 5. Daily workflow

### Evening (~15–30 min) — HPG8 on
1. Triage backlog (optional: with GrokBot).
2. Put 1–3 Issues in current Iteration; label `loop:ready`.
3. Ensure hg61 is awake (or WOL). HPG8 may sleep after.

### Night — hg61
1. `loopctl` cron ticks (e.g. every 20 min in night window).
2. Advance `loop:ready` → spec → code → review → PR.
3. Enforce caps: Issues/night, Cursor usage (Cursor Models pool %), Coder rounds, wall-clock per job.
4. Logs: `~/loop/logs/`.

### Morning (~20–40 min) — HPG8 on
1. Digest PRs / failures / spend (GrokBot optional).
2. Review/merge PRs; re-label or rewrite blocked Issues.
3. hg61: leave on if more queue, else idle (suspend only after proven).

---

## 6. Machines & electricity

| Host | Role | Power |
|---|---|---|
| **HPG8** | Human, GrokBot, SSH jump | On when working; **sleep overnight** |
| **hg61** | loopctl + Cursor CLI (Tech Lead + Coder) + Docker | On for night work / active Sprint; see power policy |
| **hg62** | Research only | Off / WOL unless research running |
| **ocr1** | Optional webhook → WOL relay | Always-on sip; **not** for heavy coding |

### Power policy v1 (safer — **committed**)

**Checked 2026-09-17 on hg61 (EliteBook 840 G6, Ubuntu 24.04 server):**
- Kernel supports deep sleep (`mem` / `disk`; `s2idle [deep]`).
- **systemd `sleep.target` / `suspend.target` are MASKED** → do not rely on auto-suspend yet.
- **WOL OK** on `eth0`: Wake-on `g`, MAC `38:22:e2:cd:19:2e`.

| Rule | Behavior |
|---|---|
| Soft end (~06:30) | Stop **claiming new** Issues |
| Active Cursor CLI job | **Never** kill for the clock; finish to DoD / max rounds / wall-clock cap |
| Checkpoint | Frequent commits + label updates (lose minutes, not the night) |
| Hard ceiling (optional ~08:00) | Graceful stop → `loop:blocked` or `loop:needs-review` + “hit morning deadline” |
| Done at 1am | **Do not wait until 7am**; after queue empty + cooldown (~20–30 min) → idle eligible |
| Auto-suspend | **Only after** unmask + tested suspend → WOL → resume (Docker + Tailscale) |
| Never | `shutdown` / `kill -9` because clock hit 7:00 |

**v1.1 checklist (before auto-sleep):** unmask suspend targets → test one suspend/resume → confirm WOL from HPG8/ocr1 → then enable idle-suspend in loopctl.

---

## 7. Scripts (`~/loop/` on hg61)

| Command | Purpose |
|---|---|
| `loopctl once` | One orchestration tick |
| `loopctl watch` | Tick until queue empty or budget hit |
| `loopctl techlead N` | Cursor CLI (Tech Lead) → write/update `N-spec.md` |
| `loopctl coder N` | Cursor CLI (Coder) → plan/implement to DoD |
| `loopctl review N` | Cursor CLI (Tech Lead) → review / PR or follow-up |
| `loopctl status` | Queue, jobs, spend |
| `loopctl doctor` | `gh`, `agent` (`agent status` via CLI login), disk, docker |
| `~/loop/bin/loop-techlead N` | Current helper: headless Tech Lead run (CLI login auth, `--model ${LOOP_MODEL:-composer-2.5}`, Loop plugins via `--plugin-dir`) |
| `REPO=<repo> ~/loop/bin/loop-agent [flags] "<prompt>"` | Generic headless run (Coder / ad-hoc) with the same model, plugins and MCP disables; workspace defaults to `$PWD` |
| `~/loop/bin/loop-common.sh` | Shared settings sourced by both helpers (model, `--plugin-dir` list, personal-MCP disable list) |

Example cron (night window, soft — does **not** force power off):

```cron
*/20 22-23,0-6 * * * /home/eddie/loop/bin/loopctl once >> /home/eddie/loop/logs/cron.log 2>&1
```

### Cursor plugins (headless, since 2026-10-06)

- **Source:** https://github.com/cursor/plugins cloned to `~/loop/plugins/cursor-plugins`, **pinned to `df581122cde17e6e27686b5a448bde23e4ad4318`** (2026-10-06 12:05 AEDT). Update steps: `~/loop/plugins/README.md`.
- **How they load:** `--plugin-dir` on every run, set in `~/loop/bin/loop-common.sh` and used by `loop-agent` and `loop-techlead`. Nothing is installed account-wide (desktop Cursor unaffected). Cursor CLI has no `agent plugin install` command (only `agent plugin marketplace ...`).

| Plugin | What it gives the Loop | Notes |
|---|---|---|
| `cursor-team-kit` (trimmed) | Skills `loop-on-ci`, `fix-ci`, `review-and-ship`, `new-branch-and-pr`, `get-pr-comments`, `fix-merge-conflicts`, `check-compiler-errors`, `verify-this`, `deslop`, ...; subagent `ci-watcher` | Uses `gh` (vbz0vader-agent). Trimmed locally: TS `typescript-exhaustive-switch` rule, thermo skill/agent (thermos covers it), `control-ui`, `run-smoke-tests`, `weekly-review` (`~/loop/plugins/trim-team-kit.sh`) |
| `thermos` | Deep branch review: `thermo-nuclear-review-subagent` + `thermo-nuclear-code-quality-review-subagent` | Skills don't auto-trigger; name them in the prompt, e.g. `/thermos` before a PR |
| `agent-compatibility` | `check-agent-compatibility` + 4 review subagents (startup, validation, docs, scan) | Run once per new repo; uses `npx -y agent-compatibility@latest` (Node 24 on hg61) |

- **Personal MCP servers disabled on hg61:** `plugin-gmail-gmail`, `plugin-google-calendar-google-calendar`, `plugin-google-drive-google-drive`, `plugin-notion-workspace-notion`, `plugin-x-x`. **Why:** they come from account-level plugins and would otherwise load into every `--force` coding run — context noise plus risky write tools (send mail, X DMs/blocks) with no Loop use. They stay installed on the account; hg61 disables them with `agent mcp disable <id>`. The CLI stores that **per project** (`~/.cursor/projects/<project>/mcp-disabled.json`), so the helpers re-apply it for every workspace before each run. Account-level skill plugins (superpowers, pstack, Notion skills) still load.
- **Future add:** the `dbt` plugin from https://github.com/dbt-labs/dbt-agent-skills (marketplace `dbt-agent-marketplace` is already registered on the account) once data-engineering/dbt repos exist.

### Spec Kit (new projects, since 2026-10-06)

- **What:** GitHub Spec Kit `specify` CLI **v1.1.0** in `~/.local/bin` on hg61. It adds spec-driven skills for the Cursor CLI. Use it for **new** projects only; do not run `specify init` in vbzio.
- **Install / upgrade:** `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.1.0`
- **Init (once, in the new repo root):** `specify init --here --force --non-interactive --integration cursor-agent --script sh`. It writes `.specify/` and `.cursor/skills/speckit-<name>/SKILL.md`. Commit `.cursor/skills/` and `.specify/`; ignore the other `.cursor/` files and the machine-local files that `.specify/.gitignore` lists.
- **Skills (hyphenated names):** `/speckit-constitution` → `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` → `/speckit-tasks`. Run `/speckit-implement` only when the human releases the work.
- **Headless flags (steps that write files):** `agent -p --trust --force --model composer-2.5 --workspace <repo> "/speckit-<name> <args>"` (or `REPO=<repo> ~/loop/bin/loop-agent "/speckit-<name> <args>"`). Do **not** use `--mode ask`: ask mode is read-only. `/speckit-clarify` asks one question at a time; headless, tell it not to wait and to write every open question (2–4 options + a recommended option, marked PROVISIONAL in the spec) to `specs/<feature>/clarifications.md`.
- **Issues:** the Tech Lead uses `gh` (vbz0vader-agent) to make GitHub Issues from `tasks.md`. Do not use `/speckit-taskstoissues`: it needs a GitHub MCP server, and Loop runs on hg61 have none.
- **Artifacts:** new projects use `specs/NNN-name/{spec,plan,tasks}.md` in place of `docs/tasks/N-spec.md` and `N-plan.md`; the constitution is `.specify/memory/constitution.md`.

### Build on hg61, deploy to hg62 (since 2026-10-06)

Use this split for projects that run on hg62 (first project: `shs-miner`).

| Step | Host | Rule |
|---|---|---|
| Code | hg61 | Cursor CLI writes the code on hg61 only. |
| Test | hg61 | Tests run on hg61. Integration tests use a disposable PostgreSQL 16 in Docker (testcontainers or docker compose). |
| Publish | GitHub | Push to `main` as vbz0vader-agent. |
| Run | hg62 | hg62 is the only runtime host: PostgreSQL, SearXNG, OmniRoute, the project services and their systemd timers. |
| Deploy | hg61 → hg62 | `scripts/deploy-hg62.sh` runs from hg61 over SSH (Tailscale or LAN): `git pull` in the deploy directory (e.g. `/home/eddie/shs/`) → `uv sync` → database migrations → install or update the systemd units → restart them → smoke check. The script stops at the first failed step. |

- Do not install the runtime infrastructure on both hosts. hg61 only runs disposable Docker test containers.
- Secrets stay in mode-600 env files on hg62. The deploy script does not copy or print them.

---

## 8. Token & $ economy

| Budget | Use | Cap idea |
|---|---|---|
| Cursor Pro ($20/mo, edc898 account) | **All** LLM work: Tech Lead spec/review + Coder implementation via Cursor CLI | Default `composer-2.5` (Cursor Models pool); watch pool % on cursor.com/dashboard/usage; escalate model per Issue only when needed |
| Electricity | hg61 when working; sleep HPG8/hg62 | No untested 7am power cut |

### Model policy (2026-10-06)

- **Default coding model: `composer-2.5`** (Tech Lead + Coder). Set in `~/.cursor/cli-config.json` and passed explicitly by `loop-techlead` / `loop-agent`. Note: if `hasChangedDefaultModel` is false in cli-config.json the CLI adopts the server default (Auto) at startup; any `--model` run writes the chosen model back.
- **Why:** cheapest model in Cursor's **Cursor Models** pool — $0.50 input / $0.20 cache read / $2.50 output per 1M tokens vs $2 / $0.50 / $6 for Grok 4.7 / 4.6 / 4.5 — and that pool has "significantly more included usage" on Pro than the $20 Other Models pool. It is Cursor's own coding model. Source: https://cursor.com/docs/models
- **Avoid `-fast` variants** (e.g. Composer 2.5 Fast = $3 / $15; Grok fast = 2x).
- **Cheaper per token but billed to the $20 Other Models pool:** `gpt-5.6-luna-*` ($0.20 / $1.20), `gpt-5.4-nano-*` ($0.20 / $1.25), `gpt-5-mini` ($0.25 / $2). Fallback only if the Cursor Models pool runs out.
- **Escalation (per Issue, not default):** `grok-4.7-low` / `cursor-grok-4.6-low` (same pool, ~4x Composer input price) for harder Issues.
- **Auto is not free:** every Auto mode bills at the list price of the model it routes to (same source).
- **OpenRouter / SiliconFlow:** no longer used for coding.
- **Headless auth:** Cursor CLI login session (`agent login`; `agent about` reports edc898@gmail.com, Pro). The helpers `unset CURSOR_API_KEY`, so the old `~/.config/cursor/api-key.env` (still sourced by interactive `~/.bashrc`) is not used.

**Effectiveness = economy:** small Issues, testable DoD, max ~2 review rounds then `loop:blocked`, put context in `spec.md` so the Coder doesn’t re-ingest the whole repo.

---

## 9. Identity split (critical)

| Account | Use for | Do not use for |
|---|---|---|
| **edc898@gmail.com** | Personal daily driver, bills, Cursor Pro / Grok payment, **all Cursor CLI model usage** (CLI login / API key) | Agent GitHub, venture Gmail/Drive, coding bots’ git identity |
| **vbz0vader@gmail.com** | Agentic development, **vbzio.com** venture: GitHub (**vbz0vader-agent**), Gmail, Google Drive, `gh`, Cursor CLI git identity | Personal bills / private mail |

All coding / `gh` / loop PRs / Drive used by agents: **vbz0vader@gmail.com** only. Cursor usage is billed to edc898’s Cursor Pro, but that does **not** mean agents authenticate to GitHub as edc898 — never use edc898 for GitHub.

**vbzio.com** is the long-term path from employment income to online income; this Loop exists to ship that venture.

---

## 10. Implementation order (when we build)

1. Create GitHub Project + labels + one pilot repo with `docs/tasks/`.
2. ~~Install Pi on hg61; wire OpenRouter (and SiliconFlow as needed).~~ Superseded 2026-10-06: Cursor CLI is also the Coder (no separate coding agent or third-party API keys).
3. Confirm `gh` auth as vbz0vader; Cursor CLI already present (default model `composer-2.5`).
4. Scaffold `~/loop` + `loopctl` (once / techlead / coder / review).
5. Dry-run one Issue end-to-end while awake.
6. Enable night cron (soft window).
7. Later: suspend unmask + WOL test → idle-suspend.

---

## 11. Agent quick reference

**Tech Lead prompt intent:** Understand Issue; write only `docs/tasks/N-spec.md` with requirements and DoD checklist; create child Issues for the Coder (Cursor CLI); do not implement product code.

**Coder prompt intent (Cursor CLI, `composer-2.5`):** Implement only that spec; write `N-plan.md` then code/tests until DoD; write `N-walkthrough.md`; commit often; stop when DoD met or round/wall-clock cap hit.

**Human morning:** Review PRs labeled `loop:pr-open`; ignore sleeping machines if GitHub state is complete.

---

## 12. Changelog

- **2026-10-06 — Build on hg61, deploy to hg62:** Added §7 subsection. Cursor CLI writes code and runs tests on hg61 (disposable PostgreSQL 16 in Docker), pushes to `main`; hg62 is the only runtime host; `scripts/deploy-hg62.sh` deploys over SSH (git pull, `uv sync`, migrations, systemd units, restart, smoke check). First project: `shs-miner`.
- **2026-10-06 — Spec Kit:** Added GitHub Spec Kit `specify` v1.1.0 (integration `cursor-agent`, hyphenated `/speckit-*` skills) for new projects (see §7 Spec Kit). New projects use `specs/NNN-name/{spec,plan,tasks}.md` in place of `docs/tasks/N-spec.md` / `N-plan.md`; the Tech Lead makes Issues from `tasks.md` with `gh` (no `/speckit-taskstoissues`, which needs a GitHub MCP server). vbzio is not initialised with Spec Kit.
- **2026-10-06 — Cursor plugins:** Added pinned `cursor/plugins` checkout (`df58112`) at `~/loop/plugins/cursor-plugins`; `cursor-team-kit` (trimmed), `thermos`, `agent-compatibility` load via `--plugin-dir` (see §7 Cursor plugins). New `~/loop/bin/loop-agent` + `loop-common.sh`; `loop-techlead` now uses CLI login auth (no API key file) and the plugin set. Account plugins' personal MCP servers (Gmail, Calendar, Drive, Notion, X) disabled for hg61 runs via `agent mcp disable`. Default model confirmed `composer-2.5` (`agent about`).
- **2026-10-06 — stack simplification:** Coding stack reduced to GrokBot + Cursor CLI. Pi (former Coder), OpenHands and OpenAI Codex CLI removed from hg61. Cursor CLI (`~/.local/bin/agent`) now does **both** Tech Lead and Coder. OpenRouter / SiliconFlow no longer used for coding. Default model `composer-2.5` (cheapest Cursor Models pool model; see §8). All usage on Cursor Pro (edc898); GitHub stays vbz0vader-agent. `~/.cursor/cli-config.json` default model set (backup `cli-config.json.bak`); `~/loop/bin/loop-techlead` passes `--model` and sources the API key; `~/loop/bin/README.md` updated.
- **2026-09-17 —** Approved blueprint (Approach A), power policy v1.
