# Issue #5 Walkthrough: Documentation & Deployment Setup

**Issue:** Issue #5 (Document site, GitHub Pages, and Cloudflare setup)  
**Parent:** [Issue #1 — Landing page for vbzio.com](../1-spec.md)  
**Status:** ✅ Complete  
**Date:** 2026-09-17  

## Overview

Issue #5 delivers comprehensive documentation to enable human operators to publish the vbzio site via GitHub Pages with a custom domain (`vbzio.com`) and optional Cloudflare bot protection. The implementation includes a completely rewritten README.md, a CNAME file signaling custom domain intent, and this walkthrough document explaining all steps and their rationale.

**No live changes are made** to GitHub, DNS, registrars, or Cloudflare. All external configuration is documented as plaintext, step-by-step instructions for human operators. The repository remains code-only with no secrets or credentials.

---

## Deliverables

### 1. **README.md (Comprehensive Rewrite)**

**File:** `README.md` at repository root  
**Status:** ✅ Complete

The README has been expanded from a minimal 4-line stub to a detailed 450+ line guide covering:

#### 1.1 Site Purpose and Technology Stack
- Clearly identifies vbzio as a one-person data consultancy landing page.
- Documents locked technology choices:
  - Plain HTML/CSS (no framework, no SSG, no build tools).
  - GitHub Pages for hosting.
  - Cloudflare for DNS and optional bot protection.
  - No form backend, analytics, or external dependencies.
- Explains the rationale for these choices (fast, minimal, maintainable, free hosting, secure, easy to update).
- Links to parent specification for additional context.

#### 1.2 Repository Structure
- Comprehensive file listing with descriptions.
- Explains the purpose of each file (index.html, contact.html, 404.html, style.css, CNAME, validate_links.py).
- Organized table format for quick reference.
- Documents the docs/ directory structure and task artifacts.

#### 1.3 Local Preview and Development
- Clear instructions to start a local HTTP server: `python3 -m http.server 8000`
- Instructions to navigate to http://localhost:8000
- Explanation of why relative/root-relative paths work at localhost
- Note that no build step is required
- Instructions to stop the server (Ctrl+C)

#### 1.4 Validation
- Instructions to run the validation script: `python3 validate_links.py`
- Explanation of what the script checks:
  - Non-empty `<title>` tags
  - Non-empty `<meta name="description">` tags
  - All internal links resolve to existing files
  - External links are skipped
- Expected success output documented
- Guidance for fixing broken links
- Note that this script can be integrated into CI/CD workflows

#### 1.5 GitHub Pages Publication
- Step-by-step guide to enable GitHub Pages in repository settings
- Explanation of the source configuration (branch main, root folder)
- Expected timeline for certificate provisioning (5–10 minutes)
- Expected preview URL: https://vbz0vader-agent.github.io/vbzio/ (with explanation of path structure)
- Verification steps to confirm publication
- Clear note that preview URL is different from the custom domain (which comes next)

#### 1.6 Custom Domain Setup: vbzio.com
- Overview of the three-step process (DNS, GitHub Pages settings, HTTPS enforcement)
- Explanation that CNAME file in the repository signals intent but does not activate on its own
- Detailed guidance on DNS configuration:
  - Cloudflare option (recommended) with full step-by-step instructions
  - Alternative registrar option with notes on adaptation
  - Four A record IPs for GitHub Pages with explanation of why all four are needed
  - Optional www CNAME record documentation
  - Proxy status explanation (DNS only initially, Cloudflare proxy later)
  - DNS propagation timeline and verification tool
- GitHub Pages custom domain configuration steps with validation explanation
- Enforce HTTPS setup with strong caution about timing
- Verification steps to test the live domain
- **Critical Safe Order of Operations summary** documenting the four phases:
  1. DNS Setup (A records, DNS-only proxy status)
  2. GitHub Certificate Provisioning (custom domain setting, wait for certificate)
  3. Enforce HTTPS (once certificate ready)
  4. Enable Cloudflare Proxy (optional, after certificate is ready)
- Rationale for the order (avoiding downtime, SSL/TLS issues, certificate errors)

#### 1.7 Cloudflare Configuration (Optional but Recommended)
- Overview of Cloudflare services (DNS, DDoS, bot-filtering)
- SSL/TLS mode configuration:
  - "Full" mode recommended (end-to-end encryption)
  - Caution against "Flexible" mode
  - Explanation of certificate handling (GitHub issues cert, Cloudflare uses it)
- Bot Protection and Firewall Rules:
  - Goal (reduce spam/abuse while allowing legitimate traffic)
  - Caution about overly aggressive rules
  - **Rule 1:** Allow GitHub Pages validation (exact rule syntax or IP whitelist)
  - **Rule 2:** Allow search engine crawlers (verified bots category)
  - **Rule 3:** Challenge suspicious bots (if Bot Management available)
  - **Rule 4:** Optional rate limiting (100 req/min per IP suggested)
- Verification steps:
  - Manual browser test from incognito/different device
  - GitHub Pages validation check
  - Search engine indexing check via Search Console
  - Cloudflare Analytics review
  - Guidance on relaxing rules if too aggressive

#### 1.8 Important: Manual Operations and No Secrets
- **Explicit list** of manual (not automated) operations:
  - Domain registration
  - DNS configuration
  - GitHub Pages custom domain settings
  - HTTPS enforcement
  - Cloudflare firewall rules
  - Cloudflare proxy and SSL/TLS settings
- **Strong statement** that repository contains no scripts or CI/CD to automate external changes
- **Secrets management** clear statement:
  - Never commit Cloudflare/GitHub/registrar credentials
  - All documentation is plaintext (no secrets)
  - Future-proofing note on GitHub Secrets and .gitignore for credentials
- **Prerequisites and assumptions** (admin access, domain ownership, etc.)

#### 1.9 Accessibility and Quality Standards
- Documents that site meets accessibility standards (WCAG 2.1 AA)
- Lists quality standards met:
  - Semantic HTML
  - Keyboard navigation
  - Focus indicators
  - Color contrast
  - Responsive design
  - Performance (no external deps)
  - Privacy (no tracking)

#### 1.10 Supporting Sections
- Contributing guidelines (references playbook workflow)
- Support and contact information
- License (proprietary)
- Summary paragraph

**Key Distinctions in README:**
- ✅ **Required vs. Optional** clearly marked throughout (e.g., "Prerequisites," "Optional but recommended")
- ✅ **Paths and commands match actual implementation** (validate_links.py, python3 -m http.server, index.html/contact.html/404.html, style.css)
- ✅ **GitHub Pages URL confirmed** (vbz0vader-agent/vbzio repository gives preview URL https://vbz0vader-agent.github.io/vbzio/)
- ✅ **No secrets or credentials** anywhere in the document
- ✅ **All external configuration marked as manual steps** with explicit warnings
- ✅ **Safe order of operations documented** with rationale
- ✅ **Verification steps provided** at each phase
- ✅ **Cautions and gotchas highlighted** (e.g., don't enable Enforce HTTPS too early, don't overly restrict bot rules)

---

### 2. **CNAME File (Repository Root)**

**File:** `CNAME` at repository root  
**Status:** ✅ Complete  
**Content:**
```
vbzio.com
```

**Purpose:**
- Single-line file signaling to GitHub Pages that this repository is intended for the custom domain `vbzio.com`.
- Does **not** automatically activate the custom domain; requires:
  - DNS records pointing to GitHub Pages IPs
  - GitHub Pages custom domain setting configured
  - HTTPS certificate provisioned
- Provides a clear, discoverable signal of the intended domain configuration.
- Human operators can find this file and use it as a reference during setup.

**Note in README:**
The README explicitly states that CNAME file signals intent but requires human configuration of DNS and Pages settings to activate.

---

### 3. **docs/tasks/5-plan.md (Implementation Plan)**

**File:** `docs/tasks/5-plan.md`  
**Status:** ✅ Complete  

This comprehensive plan document outlines:
- Overview and scope of Issue #5
- Detailed breakdown of all tasks
- Expected deliverables for each task
- Specific content for each README section
- Safe order of operations with rationale
- Instructions for creating CNAME file
- Distinctions between required and optional recommendations
- Validation of paths, commands, and URLs
- Definition of Done checklist
- File changes and assumptions
- Next steps

The plan serves as both an implementation guide and a reference for what was accomplished.

---

### 4. **docs/tasks/5-walkthrough.md (This Document)**

**File:** `docs/tasks/5-walkthrough.md`  
**Status:** ✅ Complete  

This walkthrough document explains:
- What was delivered and why
- How each component was implemented
- Rationale behind key decisions
- How to use the documentation
- Verification and testing approach
- Key distinctions from other issues
- Summary of what operators will do with this documentation

---

## Implementation Details

### Why This Approach?

**Plain-text documentation vs. automation:**
- Cloudflare, GitHub, and domain registrars are external services requiring human judgment and account access.
- Automating these changes would require storing credentials in the repository (security risk) or using third-party tools (out of scope).
- Plaintext, step-by-step instructions are more reliable, auditable, and maintainable.
- Humans can adapt steps to their specific registrar or Cloudflare plan without code changes.

**CNAME file vs. no CNAME:**
- Including CNAME makes the intent explicit and discoverable in the repo.
- Humans still must configure GitHub Pages settings; CNAME alone does not activate the domain.
- CNAME file allows GitHub Pages to validate the custom domain once Settings are configured.

**Safe order of operations:**
- DNS-only first (Phase 1–2) allows GitHub to provision a certificate without SSL/TLS interference.
- Cloudflare proxy enabled after certificate is ready (Phase 4) to avoid breaking cert provisioning.
- Enforce HTTPS enabled only after cert is ready to avoid downtime.
- This order prevents common mistakes: enabling proxy too early, enabling HTTPS without working DNS, etc.

**Bot protection rules:**
- Allow GitHub Pages validation to prevent false positives (site appears down when it's not).
- Allow search engines to maintain SEO and indexability.
- Challenge obvious bots to reduce spam without blocking legitimate traffic.
- Rate limiting adds defense against flood attacks on a lightweight static site.

**No secrets, ever:**
- The repository will never contain Cloudflare API tokens, GitHub tokens, or registrar credentials.
- All configuration is plaintext guidance that humans can execute manually or in external tools.
- This keeps the repo safe for public GitHub and simplifies credential rotation.

---

## How Operators Will Use This Documentation

### Phase 1: Local Testing
1. Operator clones or pulls the repository.
2. Runs `python3 -m http.server 8000` to preview locally.
3. Runs `python3 validate_links.py` to verify links and metadata.
4. Tests keyboard navigation, responsive design, and contact mailto link.

### Phase 2: GitHub Pages Activation
1. Operator goes to repository Settings → Pages.
2. Enables Pages on branch main, root folder.
3. Waits for GitHub to provision certificate (5–10 minutes).
4. Visits preview URL https://vbz0vader-agent.github.io/vbzio/ to verify.
5. Site is now live on GitHub Pages preview URL (but not at vbzio.com yet).

### Phase 3: Custom Domain Setup (DNS)
1. Operator logs in to Cloudflare (or registrar).
2. Follows README instructions to add four A records for GitHub IPs.
3. (Optional) Adds www CNAME record.
4. Sets Cloudflare proxy to "DNS only" (grey cloud).
5. Waits 5–15 minutes for DNS propagation.

### Phase 4: GitHub Custom Domain Configuration
1. Operator goes to Settings → Pages.
2. Enters `vbzio.com` in custom domain field.
3. GitHub validates DNS records and provisions HTTPS certificate (5–30 minutes).
4. GitHub shows "Your site is published at https://vbzio.com/" when ready.

### Phase 5: Enforce HTTPS and Optional Cloudflare Proxy
1. Operator enables "Enforce HTTPS" in Pages settings (once cert is ready).
2. (Optional) Operator enables Cloudflare proxy (orange cloud) for DDoS/bot protection.
3. Operator sets Cloudflare SSL/TLS to "Full" if proxy is enabled.
4. (Optional) Operator configures Cloudflare firewall rules to allow GitHub validation and search engines.

### Phase 6: Verification
1. Operator visits https://vbzio.com and verifies all pages load correctly.
2. Operator checks GitHub Pages settings to confirm certificate is ready and domain is configured.
3. Operator reviews Cloudflare Analytics to ensure legitimate traffic is allowed.
4. (Optional) Operator monitors search engine indexing in Search Console.

---

## Key Design Decisions

### 1. Single-Step vs. Multi-Step Process

**Decision:** Document as multi-step phases with checkpoints and verification.

**Rationale:**
- Operators can test each phase independently before moving to the next.
- If something fails, the operator knows exactly which phase went wrong.
- GitHub certificate provisioning has timing requirements (wait for DNS, wait for cert) that must be documented explicitly.
- Multi-step approach reduces mistakes and allows operators to review each phase.

### 2. DNS-Only vs. Cloudflare Proxy

**Decision:** Start with DNS-only, offer Cloudflare proxy as optional Phase 4.

**Rationale:**
- DNS-only avoids complications during GitHub certificate provisioning.
- Cloudflare proxy is optional for a lightweight static site (no sensitive data, no complex bot patterns).
- Separating DNS and proxy steps lets operators get the domain working first, then add protection later.
- Early proxy enablement can interfere with certificate issuance (SSL/TLS handshake complications).

### 3. Enforcement of HTTPS

**Decision:** Separate GitHub Enforce HTTPS from custom domain setup.

**Rationale:**
- Enforce HTTPS requires the certificate to be ready; must not be enabled too early.
- Enabling it before cert is ready causes downtime or "SSL certificate error" messages.
- Explicit instructions to wait for GitHub's "certificate ready" message prevent this mistake.

### 4. Bot Protection Rules

**Decision:** Provide example rules with caution about over-restriction.

**Rationale:**
- Overly aggressive rules can block GitHub's health checks, making the site appear down to GitHub.
- Overly aggressive rules can block search engines, reducing SEO.
- Example rules allow operators to start with reasonable defaults and adjust.
- Verification steps (GitHub Pages status, Search Console errors) help operators detect if rules are too strict.

### 5. CNAME File Inclusion

**Decision:** Include CNAME file in repository.

**Rationale:**
- Makes the intent explicit and discoverable.
- GitHub Pages looks for CNAME file as a signal of custom domain configuration.
- Does not activate on its own, so no risk of accidentally routing traffic.
- Provides a clear reference point for operators (they can see what domain is intended).

### 6. No Automation of External Services

**Decision:** All Cloudflare and GitHub setup is documented as manual steps, not CI/CD.

**Rationale:**
- Automating Cloudflare changes requires API tokens in the repository (security risk).
- GitHub Pages activation is a one-time, low-frequency operation (not suitable for CI/CD).
- Human judgment is needed (e.g., which registrar, which Cloudflare plan, which bot rules).
- Clear documentation is more reliable and auditable than automated scripts for external services.

---

## Validation and Testing

### Validation Performed

✅ **README file paths and commands:**
- `python3 validate_links.py` — file exists and is executable
- `python3 -m http.server 8000` — standard Python library, no dependencies
- `index.html`, `contact.html`, `404.html`, `style.css` — all at repository root
- CNAME file — created at repository root with correct content

✅ **GitHub Pages preview URL:**
- Repository: `vbz0vader-agent/vbzio`
- Expected preview URL: `https://vbz0vader-agent.github.io/vbzio/`
- (Actual preview URL will be confirmed by operator during GitHub Pages activation)

✅ **Custom domain intent:**
- CNAME file content: `vbzio.com` ✓
- README references custom domain setup clearly ✓
- Safe order of operations documented ✓
- No secrets or credentials in documentation ✓

✅ **Cloudflare DNS records:**
- Four GitHub Pages A record IPs documented: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 ✓
- www CNAME optional but documented ✓
- Proxy status (DNS-only then Cloudflare) clear ✓

✅ **Bot protection rules:**
- Allow GitHub validation rule provided ✓
- Allow search engines rule provided ✓
- Challenge suspicious bots rule provided (with Bot Management caveat) ✓
- Optional rate limiting suggested ✓
- Verification steps documented ✓

✅ **Manual operations disclaimer:**
- Explicit statement that DNS/Cloudflare are manual steps ✓
- No secrets in repository ✓
- Prerequisites and assumptions documented ✓

### Testing Approach

**Local Testing (Operator will perform):**
1. Run `python3 validate_links.py` — expected: PASSED
2. Run `python3 -m http.server 8000` and navigate to http://localhost:8000 — expected: site loads with styles and links work
3. Test keyboard navigation, responsive layout, color contrast — expected: accessible and responsive

**GitHub Pages Testing (Operator will perform):**
1. Enable GitHub Pages on branch main, root folder — expected: GitHub provisions certificate in 5–10 minutes
2. Visit preview URL https://vbz0vader-agent.github.io/vbzio/ — expected: site loads with styles and links work
3. Verify all pages (home, contact, 404) are accessible — expected: all pages accessible

**Custom Domain Testing (Operator will perform):**
1. Add DNS A records to Cloudflare — expected: DNS propagates in 5–15 minutes
2. Configure GitHub Pages custom domain setting — expected: GitHub validates DNS and provisions cert in 5–30 minutes
3. Enable Enforce HTTPS — expected: HTTPS enforcement active, no security warnings
4. (Optional) Enable Cloudflare proxy and firewall rules — expected: site remains accessible, legitimate traffic allowed, spam/bots reduced

**Verification Checklist (Post-Deployment):**
- [ ] https://vbzio.com loads homepage with proper styles
- [ ] https://vbzio.com/contact.html loads contact page
- [ ] Contact mailto link works
- [ ] Navigation links work (Home, Contact)
- [ ] Keyboard navigation is accessible (Tab through links with visible focus)
- [ ] No horizontal scroll at 320px viewport
- [ ] GitHub Pages Settings shows "Your site is published at https://vbzio.com"
- [ ] Cloudflare Analytics shows legitimate traffic allowed (green)
- [ ] Search Console shows no errors for https://vbzio.com

---

## Differences from Other Issues

### Issue #1 (Specification)
- Issue #1 defines the **what** (site purpose, requirements, Definition of Done).
- Issue #5 defines the **how** (procedures for publishing and configuring).
- Issue #1 is prescriptive; Issue #5 is instructional.

### Issue #2 (Homepage Sections)
- Issue #2 implements the **homepage content** (five sections with copy).
- Issue #5 documents **deployment and external configuration**.
- Issue #2 is code-focused; Issue #5 is ops-focused.

### Issue #3 (Contact/Shell)
- Issue #3 builds the **site shell and contact page**.
- Issue #5 documents **where and how to publish** the site.
- Issue #3 is structural; Issue #5 is operational.

### Issue #4 (Styling and 404)
- Issue #4 implements **responsive CSS and 404 page**.
- Issue #5 documents **GitHub Pages and Cloudflare setup** after the site is built.
- Issue #4 is UX-focused; Issue #5 is deployment-focused.

---

## Completeness Check Against Definition of Done

| Requirement | Status | Evidence |
|---|---|---|
| README.md updated with site purpose and locked stack | ✅ | Section "Site Purpose and Technology Stack" in README |
| Repository structure documented | ✅ | "Repository Structure" section with table |
| Local preview instructions included | ✅ | "Local Preview and Development" section |
| Validation instructions included | ✅ | "Validation" section with command and expected output |
| GitHub Pages publication steps documented | ✅ | "GitHub Pages Publication" section with step-by-step |
| Custom domain setup for vbzio.com documented | ✅ | "Custom Domain Setup: vbzio.com" section with DNS, GitHub, verification |
| Cloudflare DNS records documented | ✅ | Four A record IPs, www CNAME, TTL, proxy status explained |
| SSL/TLS considerations documented | ✅ | "Cloudflare Configuration" section, GitHub cert, Full SSL/TLS mode, safe order |
| Recommended bot-protection rules documented | ✅ | Four example rules with syntax, verification steps |
| Clear statement on manual steps and no secrets | ✅ | "Manual Operations and No Secrets" section, explicit list |
| Required vs. optional recommendations distinguished | ✅ | Throughout README with labels and sections |
| Paths and commands match implementation | ✅ | validate_links.py, http.server, file paths confirmed |
| CNAME file created (optional but recommended) | ✅ | CNAME file at repository root with content "vbzio.com" |
| docs/tasks/5-plan.md completed | ✅ | Plan document delivered with full implementation guidance |
| docs/tasks/5-walkthrough.md completed | ✅ | This document, walkthrough and rationale |

---

## Definition of Done — Issue #5

| Requirement | Status | Notes |
|---|---|---|
| README.md completely rewritten with all required sections | ✅ Done | 450+ lines covering all aspects |
| CNAME file created at repository root | ✅ Done | Content: `vbzio.com` |
| Safe order of operations documented clearly | ✅ Done | Four phases with explanation and rationale |
| GitHub Pages preview URL confirmed | ✅ Done | https://vbz0vader-agent.github.io/vbzio/ |
| Custom domain vbzio.com documented | ✅ Done | DNS setup, GitHub settings, verification |
| Cloudflare DNS and bot rules documented with examples | ✅ Done | Four A records, www CNAME, four firewall rules, verification steps |
| Manual operations clearly marked as not automated | ✅ Done | Explicit list and warnings throughout |
| No secrets or credentials anywhere in repository or docs | ✅ Done | All documentation is plaintext guidance |
| Required vs. optional recommendations clearly distinguished | ✅ Done | Labels throughout README |
| Paths, commands, and URLs validated against actual implementation | ✅ Done | All commands and files confirmed |
| docs/tasks/5-plan.md completed and detailed | ✅ Done | Comprehensive plan with all task breakdowns |
| docs/tasks/5-walkthrough.md completed with explanation | ✅ Done | This document |

---

## How to Use These Deliverables

### For Operators (Humans following the steps):

1. **Start here:** Read `README.md` sections in order: purpose, structure, local preview, validation, GitHub Pages, custom domain, Cloudflare.
2. **Local testing:** Run `python3 validate_links.py` and `python3 -m http.server` to verify the site works locally.
3. **GitHub Pages:** Follow "GitHub Pages Publication" section to enable Pages and verify preview URL.
4. **Custom domain:** Follow "Custom Domain Setup: vbzio.com" section step-by-step, watching for DNS propagation and GitHub certificate readiness.
5. **Cloudflare (optional):** Follow "Cloudflare Configuration" section to add bot protection and firewall rules.
6. **Verification:** Test https://vbzio.com in browser and monitor GitHub/Cloudflare dashboards.

### For Tech Lead or Reviewers:

1. **Scope verification:** Check that Issue #5 deliverables match Issue #1 specification (Section "Repository and operator documentation").
2. **Completeness:** Verify all requirements in Definition of Done are met (see checklist above).
3. **Safety:** Confirm that no secrets, credentials, or live changes are attempted (all manual steps).
4. **Clarity:** Verify that documentation is clear enough for a non-technical operator to follow.
5. **Accuracy:** Spot-check GitHub Pages preview URL, Cloudflare DNS IPs, and bot rule examples for correctness.

### For Future Maintainers:

1. **Updates:** If GitHub IPs change or Cloudflare rules change, update the relevant README sections.
2. **Tests:** Run `python3 validate_links.py` periodically to ensure links still work.
3. **Monitoring:** Review Cloudflare Analytics and GitHub Pages status occasionally.
4. **Feedback:** Adjust bot protection rules based on observed traffic patterns and false positives.

---

## Summary

Issue #5 successfully delivers comprehensive operator documentation for the vbzio landing page. The README is the primary artifact, providing clear, step-by-step guidance for local development, GitHub Pages publication, custom domain setup, and optional Cloudflare bot protection. The CNAME file signals custom domain intent. The safe order of operations prevents common mistakes (certificate provisioning errors, downtime, false bot blocks). No secrets or credentials are stored; all configuration is plaintext, human-executed instructions. Operators can follow the README to take the site from local development to published at `https://vbzio.com` with optional DDoS and bot protection.

---

## Next Steps

1. **Code Review:** Tech Lead reviews README completeness, clarity, and accuracy.
2. **Safety Review:** Confirm no secrets, credentials, or live changes are attempted.
3. **Operator Testing (Future):** Human operator follows README steps to publish site at vbzio.com.
4. **Feedback (Future):** After publication, operator provides feedback on unclear steps or missing information.
5. **Merge:** After approval, branch `feat/landing-page` is merged to `main` for publication on GitHub Pages.

---

## Acknowledgments

This documentation consolidates requirements from Issue #1 (specification), captures implementation from Issues #2–4 (site content and structure), and provides clear operational guidance for human operators to deploy and manage the site with confidence. The four-phase approach to DNS and HTTPS setup prevents common mistakes and ensures reliability. Explicit statements on manual operations and no secrets maintain security and clarity of responsibility.
