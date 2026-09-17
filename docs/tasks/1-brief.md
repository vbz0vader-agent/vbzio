# Issue #1 Brief — Landing page for vbzio.com (Loop dry-run #1)

**Issue:** https://github.com/vbz0vader-agent/vbzio/issues/1  
**Project:** https://github.com/users/vbz0vader-agent/projects/1  
**Author of this brief:** GrokBot (PO/control plane)  
**Date:** 2026-09-17 (AEST)

## PO locked decisions

| Decision | Choice |
|---|---|
| Stack | GitHub Pages from this repo (plain HTML/CSS or minimal static generator — Tech Lead chooses within “simple static”) |
| Contact | `mailto:vbz0vader@gmail.com` only (no form backend in v1) |
| Bot protection | Cloudflare in front of `vbzio.com` (document DNS/Pages + bot rules; human applies Cloudflare) |
| Theme | Light, modern, simple |
| Identity | All GitHub work as **vbz0vader-agent** / `vbz0vader@gmail.com` |

## Site structure (v1)

1. **Home `/`** — one-pager: Hero (solo data consulting), Services (data engineering, ETL, warehousing, reporting), Skills (Python, Airflow, dBT, SQL, etc.), About (one-person company), CTA → Contact
2. **Contact** — short copy + primary mailto (optional subject prefill)

## Out of scope (v1)

Form backend, Turnstile, blog, auth, CMS, payments, dark mode.

## Acceptance (parent)

- [ ] Light one-pager + contact mailto works on GitHub Pages preview URL
- [ ] README documents GitHub Pages + Cloudflare custom domain / bot-rules steps
- [ ] Child Issues created by Tech Lead with clear handoffs for Pi
- [ ] PR(s) opened with `loop:needs-review` when ready

## Tech Lead handoff

1. Read `docs/Loop-Engineering-Playbook.md` and Issue #1.
2. Write `docs/tasks/1-spec.md` with Definition of Done (do **not** implement the site).
3. Create child Issues for Pi (scaffold Pages, homepage, contact, README/Cloudflare).
4. Labels: parent `loop:ready` → `loop:specced`; children get `loop:ready`.
5. Do not write application code — Pi builds.

## Notes for dry-run #1

- Playbook also at `~/loop/docs/Loop-Engineering-Playbook.md` on hg61.
- Cursor CLI Tech Lead: `~/.local/bin/agent` (print/force/yolo for unattended).
- Coder: Pi on OpenRouter (cheap models).
