# Loop Engineering Playbook

**Status:** Approved blueprint (Approach A) — v1 power = soft window only  
**Last updated:** 2026-09-17 (AEST)  
**Canonical human copy:** Obsidian `localdev` → Development Structure → Loop  
**Agent copy:** hg61 `~/loop/docs/Loop-Engineering-Playbook.md` (keep in sync)  
**Homelab inventory:** Notion → Technology → Home Servers (not this doc)

When Cursor CLI (Tech Lead) or Pi (Coder) needs process context, **read this file first**.

---

## 1. Goal

Overnight, unattended software delivery loop:

1. Human sets goals and GitHub Issues in a Sprint.
2. **Tech Lead** (Cursor CLI) turns Issues into small specs + Definition of Done.
3. **Coder** (Pi on OpenRouter/SiliconFlow cheap models) implements and tests until DoD.
4. Tech Lead reviews; opens a PR for human morning review.

Optimize for **effectiveness** and **economy** (Cursor Pro quota, API $, electricity).

---

## 2. Roles

| Role | Actor | Responsibilities | Out of scope |
|---|---|---|---|
| Product Owner | Human (Eddie) | Priorities, sprint scope, morning PR review/merge, product unblock | Overnight coding |
| Control plane | GrokBot on HPG8 (daytime) | Help write Issues, board hygiene, quotas, lab ops, morning digest | Long unattended code loops |
| Tech Lead | Cursor CLI `agent` on hg61 | Context → break down Issue → `N-spec.md` + DoD → review plan/diff → follow-ups or `gh pr create` | Bulk cheap coding (protect Pro) |
| Coder | Pi on hg61 | `N-plan.md` → implement/test to DoD → `N-walkthrough.md` | Inventing scope; final PR without Tech Lead |
| Orchestrator | `loopctl` (no LLM) on hg61 | Labels, invoke agents, timeouts, budgets, logging | Thinking / writing product code |

**Agent count:** exactly **2 LLM agents** + **1 dumb orchestrator**.  
OpenHands optional later for rare full-sandbox jobs — **not** the default Coder.

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
| `loop:coding` | Pi working |
| `loop:needs-review` | Walkthrough ready for Tech Lead |
| `loop:changes-requested` | Tech Lead follow-up for Pi |
| `loop:pr-open` | PR awaiting human |
| `loop:blocked` | Needs human (deadline, ambiguity, failed rounds) |

### Repo artifacts (Issue `#N`)

| File | Author |
|---|---|
| `docs/tasks/N-spec.md` | Tech Lead — requirements + DoD checklist |
| `docs/tasks/N-plan.md` | Pi — implementation plan (Tech Lead may edit before coding) |
| `docs/tasks/N-walkthrough.md` | Pi — what changed, how to verify |

Issue comments = short status. **Files + PR** = source of truth for agents.

---

## 4. State machine

```
human: Issue in Sprint + loop:ready
  → loopctl claims → Cursor CLI Tech Lead
  → writes N-spec.md + DoD → loop:specced
  → loopctl starts Pi
  → Pi writes N-plan.md → (optional Tech Lead plan check)
  → Pi implement/test loop → N-walkthrough.md → loop:needs-review
  → Cursor CLI review
       ├─ fail → comment + loop:changes-requested → Pi (max rounds)
       └─ pass → gh pr create → loop:pr-open
  → human morning: review / merge
```

**Concurrency (v1):** 1 Cursor CLI session + **1** Pi job. Raise Pi concurrency only after stable.

---

## 5. Daily workflow

### Evening (~15–30 min) — HPG8 on
1. Triage backlog (optional: with GrokBot).
2. Put 1–3 Issues in current Iteration; label `loop:ready`.
3. Ensure hg61 is awake (or WOL). HPG8 may sleep after.

### Night — hg61
1. `loopctl` cron ticks (e.g. every 20 min in night window).
2. Advance `loop:ready` → spec → code → review → PR.
3. Enforce caps: Issues/night, Cursor minutes, OR/SF $, Pi rounds, wall-clock per job.
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
| **hg61** | loopctl + Cursor CLI + Pi + Docker | On for night work / active Sprint; see power policy |
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
| Active Pi/Cursor | **Never** kill for the clock; finish to DoD / max rounds / wall-clock cap |
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
| `loopctl techlead N` | Cursor CLI → write/update `N-spec.md` |
| `loopctl coder N` | Pi → plan/implement to DoD |
| `loopctl review N` | Cursor CLI → review / PR or follow-up |
| `loopctl status` | Queue, jobs, spend |
| `loopctl doctor` | `gh`, `agent`, `pi`, disk, docker |

Example cron (night window, soft — does **not** force power off):

```cron
*/20 22-23,0-6 * * * /home/eddie/loop/bin/loopctl once >> /home/eddie/loop/logs/cron.log 2>&1
```

---

## 8. Token & $ economy

| Budget | Use | Cap idea |
|---|---|---|
| Cursor Pro ($20) | Tech Lead spec + review only | Few short sessions/night; no overnight Cursor coding |
| OpenRouter / SiliconFlow | Pi loops | Nightly $ soft cap; free → cheap Flash/Qwen/DeepSeek; avoid Pro/Kimi defaults |
| Electricity | hg61 when working; sleep HPG8/hg62 | No untested 7am power cut |

**Effectiveness = economy:** small Issues, testable DoD, max ~2 review rounds then `loop:blocked`, put context in `spec.md` so Pi doesn’t re-ingest the whole repo.

---

## 9. Identity split (critical)

| Account | Use for | Do not use for |
|---|---|---|
| **edc898@gmail.com** | Personal daily driver, bills, Cursor Pro / Grok payment | Agent GitHub, venture Gmail/Drive, coding bots |
| **vbz0vader@gmail.com** | Agentic development, **vbzio.com** venture: GitHub, Gmail, Google Drive, `gh`, Pi, Cursor CLI git identity, OpenHands GitHub | Personal bills / private mail |

All coding / `gh` / loop PRs / Drive used by agents: **vbz0vader@gmail.com** only. Paying for Cursor/Grok on edc898 does **not** mean agents authenticate as edc898.

**vbzio.com** is the long-term path from employment income to online income; this Loop exists to ship that venture.

---

## 10. Implementation order (when we build)

1. Create GitHub Project + labels + one pilot repo with `docs/tasks/`.
2. Install Pi on hg61; wire OpenRouter (and SiliconFlow as needed).
3. Confirm `gh` auth as vbz0vader; Cursor CLI already present.
4. Scaffold `~/loop` + `loopctl` (once / techlead / coder / review).
5. Dry-run one Issue end-to-end while awake.
6. Enable night cron (soft window).
7. Later: suspend unmask + WOL test → idle-suspend.

---

## 11. Agent quick reference

**Tech Lead prompt intent:** Understand Issue; write only `docs/tasks/N-spec.md` with requirements and DoD checklist; do not implement product code.

**Coder prompt intent:** Implement only that spec; write `N-plan.md` then code/tests until DoD; write `N-walkthrough.md`; commit often; stop when DoD met or round/wall-clock cap hit.

**Human morning:** Review PRs labeled `loop:pr-open`; ignore sleeping machines if GitHub state is complete.
