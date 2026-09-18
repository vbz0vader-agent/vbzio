# Issue #5 Implementation Plan: Documentation & Deployment Setup

**Issue:** Issue #5 (Document site, GitHub Pages, and Cloudflare setup)  
**Parent:** [Issue #1 — Landing page for vbzio.com](../1-spec.md)  
**Status:** Planning  

## Overview

This plan outlines the comprehensive documentation updates to `README.md` that guide human operators through:
1. Local development and validation of the site.
2. GitHub Pages publication and preview URL.
3. Custom domain configuration for `vbzio.com`.
4. Cloudflare DNS, SSL/TLS, and bot-protection setup.
5. Safe operational procedures to avoid blocking legitimate traffic or GitHub Pages validation.

This issue does **not** make any live changes to GitHub, DNS, registrars, or Cloudflare. All external configuration is documented as manual steps for human operators. The repository will include a `CNAME` file documenting the custom domain intent, but requires human configuration of Pages settings and Cloudflare.

## Scope

### In Scope

1. **README.md Updates:**
   - Site purpose and technology stack (plain HTML/CSS, GitHub Pages, Cloudflare).
   - Repository structure with clear file descriptions.
   - Local preview instructions (`python3 -m http.server`).
   - Validation instructions (`python3 validate_links.py`).
   - GitHub Pages publication steps and expected preview URL.
   - Custom domain setup for `vbzio.com` (CNAME file documentation and Pages settings).
   - Cloudflare DNS records (apex `vbzio.com` and optional `www.vbzio.com`).
   - SSL/TLS considerations and safe provisioning order.
   - Recommended Cloudflare bot-protection and firewall rules.
   - Clear distinctions between required and optional recommendations.
   - Explicit statement that DNS/Cloudflare are manual steps with no secrets in repo.

2. **CNAME File (Optional but Recommended):**
   - Create `CNAME` file at repository root with content: `vbzio.com`
   - Include a note in README explaining that human must still configure GitHub Pages custom domain setting.

3. **Documentation Files:**
   - `docs/tasks/5-plan.md` — This plan (guides implementation).
   - `docs/tasks/5-walkthrough.md` — Implementation narrative (explains what was done and how).

### Out of Scope

- Live GitHub Pages, DNS, registrar, SSL/TLS, or Cloudflare account configuration.
- Creating, updating, or accessing any external service credentials.
- Testing live deployment (GitHub Pages publish, DNS resolution, Cloudflare rules).
- Form backend, analytics, or other application features.

## Tasks and Deliverables

### Task 1: Update README.md

**File:** `README.md` (replace/augment existing minimal version)

**Sections to add/expand:**

#### 1.1 Site Purpose and Technology Stack
- Brief description: vbzio is a landing page for a one-person data consultancy.
- Locked technology choices:
  - Plain HTML and CSS (no framework, no SSG, no build tools).
  - GitHub Pages for hosting.
  - Cloudflare for DNS and optional bot protection.
  - No form backend, analytics, or external dependencies.
- Link to parent issue or specification for context.

#### 1.2 Repository Structure
- List key files and folders with descriptions:
  - `index.html` — Homepage with Hero, Services, Skills, About, and CTA sections.
  - `contact.html` — Contact page with mailto link to vbz0vader@gmail.com.
  - `404.html` — Error page for GitHub Pages.
  - `style.css` — Shared light-theme stylesheet.
  - `validate_links.py` — Python script to validate local links and metadata.
  - `docs/` — Documentation and task planning.
  - `CNAME` — Custom domain configuration file (optional, see below).

#### 1.3 Local Preview
- Instructions to start a local HTTP server:
  ```bash
  python3 -m http.server 8000
  ```
- Instructions to visit `http://localhost:8000` in browser.
- Explanation that links work correctly at localhost because they use relative paths or root-relative paths that resolve from `/`.
- Note that preview will look identical to final site (no build step needed).

#### 1.4 Validation
- Instructions to run the validation script:
  ```bash
  python3 validate_links.py
  ```
- Explanation of what the script checks:
  - All HTML files have non-empty `<title>` tags.
  - All HTML files have non-empty `<meta name="description">` tags.
  - All internal links (relative and root-relative) resolve to existing files.
  - External links (`http://`, `https://`, `mailto:`) are skipped (not validated locally).
- Expected output on success: `Validation PASSED: All local links and metadata are valid.`
- Note that this is a lightweight check suitable for CI/pre-commit workflows.

#### 1.5 GitHub Pages Publication
- **Step 1:** Enable GitHub Pages in repository settings.
  - Go to repository Settings → Pages.
  - Source: Branch `main` (or `feat/landing-page` if testing on branch), root folder.
  - Save.
- **Step 2:** GitHub will provision an initial HTTPS certificate (can take a few minutes).
- **Expected preview URL:** `https://vbz0vader-agent.github.io/vbzio/`
  - Username: `vbz0vader-agent`
  - Repository: `vbzio`
  - Path: `/vbzio/` (trailing slash; GitHub Pages uses project URLs by default).
- **Verification:** Navigate to the preview URL in a browser within 5–10 minutes of enabling Pages. All pages (index, contact, 404) should load and be styled correctly.
- **Note:** At this point, the site is publicly accessible at the preview URL but **not** at `vbzio.com` yet. Custom domain setup requires additional Cloudflare and Pages configuration (see below).

#### 1.6 Custom Domain Setup (vbzio.com)

##### 6.1 Add CNAME File to Repository
- File: `CNAME` at repository root.
- Content: `vbzio.com` (one line, no trailing newline needed).
- Purpose: Signals GitHub Pages that this repository intends to serve traffic for the domain `vbzio.com`.
- Note: Creating this file in the repo does **not** automatically route traffic; human must configure DNS and Pages settings (see below).

##### 6.2 Configure GitHub Pages Custom Domain Setting
- Go to repository Settings → Pages.
- **Custom domain** field: Enter `vbzio.com`.
- GitHub will validate that the domain has appropriate DNS records pointing to GitHub (see Cloudflare section below).
- **Enforce HTTPS:** Check this box once DNS is correctly configured and GitHub certificate is provisioned.
- Save.

**Important:** Do **not** check "Enforce HTTPS" until:
1. DNS records are pointing GitHub Pages IP addresses (see Cloudflare section).
2. GitHub has successfully provisioned an HTTPS certificate (GitHub will show a message if certificate is ready).
3. The domain resolves to GitHub Pages successfully.

If you enable HTTPS too early, the site may become temporarily unreachable. The safe order is documented in section 6.3 below.

##### 6.3 Safe Order of Operations for DNS and GitHub Pages

To avoid downtime and certificate provisioning issues, follow this order:

1. **Prerequisites:** Ensure this file (`CNAME`) exists in the repository and Pages is enabled on branch `main`.

2. **Phase 1: Cloudflare Setup (DNS without proxying)**
   - Log in to Cloudflare account.
   - Add `vbzio.com` domain (or use existing zone if already in Cloudflare).
   - Create DNS records for GitHub Pages:
     - **For apex domain (`vbzio.com`):**
       ```
       Type: A
       Name: vbzio.com (or @)
       Content: 185.199.108.153
       TTL: Auto
       Proxy status: DNS only (not Cloudflare proxy, grey cloud)
       ```
       - Add three more A records (GitHub maintains multiple IP addresses for redundancy):
         - `185.199.109.153`
         - `185.199.110.153`
         - `185.199.111.153`
     - **For www subdomain (optional but recommended):**
       ```
       Type: CNAME
       Name: www
       Content: vbz0vader-agent.github.io
       TTL: Auto
       Proxy status: DNS only (grey cloud)
       ```
       - This allows `www.vbzio.com` to work as an alias to the GitHub Pages preview URL.
       - GitHub will handle redirecting www to apex if configured (see Pages settings).
   - **Proxy status:** Initially set all records to "DNS only" (grey cloud), not Cloudflare proxy (orange cloud). This allows GitHub certificate provisioning without SSL/TLS complications.
   - **TTL:** Auto (Cloudflare will optimize).
   - Save all DNS records.

3. **Phase 2: GitHub Pages Certificate Provisioning**
   - After DNS records are in place and resolving (wait 5–15 minutes for propagation), GitHub will detect the DNS configuration.
   - GitHub will automatically request and provision an HTTPS certificate for `vbzio.com`.
   - Go to repository Settings → Pages to monitor certificate status (GitHub will show "Certificate is being provisioned" or "Certificate issued").
   - Wait for the message: "Your site is published at https://vbzio.com/" — this means the certificate is ready.
   - This typically takes 5–30 minutes.

4. **Phase 3: Enable Enforce HTTPS**
   - Once GitHub confirms the certificate is ready, go to Settings → Pages.
   - Check **Enforce HTTPS** to redirect HTTP traffic to HTTPS.
   - Save.

5. **Phase 4: Enable Cloudflare Proxy (Optional)**
   - Once the site is working at `https://vbzio.com` via DNS-only mode, you may optionally enable Cloudflare proxy to add DDoS protection, bot-filtering, and caching.
   - Go to Cloudflare DNS records for `vbzio.com` (the A records for GitHub IPs).
   - Change **Proxy status** from "DNS only" (grey cloud) to "Proxied" (orange cloud) for the apex domain A records.
   - **Caution:** Cloudflare proxying may interfere with GitHub's certificate validation if enabled too early. Ensure the certificate is already issued before proxying.
   - The www CNAME can also be proxied, but typically www traffic is redirected to apex anyway.

**Why this order?**
- DNS-only (Phase 1–2) allows GitHub to validate domain ownership and provision a certificate.
- Proxying through Cloudflare (Phase 4) is added after the cert is ready to avoid SSL/TLS issues.
- Early HTTPS enforcement without working DNS can cause certificate errors or downtime.

#### 1.7 Cloudflare DNS and Bot Protection Configuration

##### 7.1 DNS Records Required

**Apex Domain A Records (for `vbzio.com`):**
```
Type: A
Name: vbzio.com (or @)
Content: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 (four separate A records)
TTL: Auto
Proxy: DNS only (grey cloud) initially; may change to Proxied (orange cloud) after certificate is ready
```

**WWW Subdomain (optional but recommended):**
```
Type: CNAME
Name: www
Content: vbz0vader-agent.github.io
TTL: Auto
Proxy: DNS only (grey cloud) initially
```

**Verification:** After DNS is set up and propagated (5–15 minutes):
- `dig vbzio.com` or `nslookup vbzio.com` should resolve to one of the GitHub A records.
- Browser navigation to `https://vbzio.com` should load the site.

##### 7.2 SSL/TLS Considerations

- **GitHub Certificate:** GitHub Pages will issue a free HTTPS certificate for custom domains (issued by Let's Encrypt). This certificate is automatic and requires no action if DNS is correctly configured.
- **Cloudflare Full SSL/TLS Mode:** If Cloudflare proxy is enabled (orange cloud), set Cloudflare's SSL/TLS mode to "Full" (not "Flexible") to ensure end-to-end encryption from client → Cloudflare → GitHub.
  - Go to Cloudflare Dashboard → SSL/TLS.
  - Set mode to "Full" or "Full (strict)" depending on your trust model.
- **No manual certificate upload required:** GitHub and Cloudflare handle certs automatically. Do not attempt to upload custom certificates unless you have specific requirements.

##### 7.3 Recommended Bot Protection and Firewall Rules

This site is static with no form backend, no authentication, and no sensitive data. Bot protection is primarily to reduce spam bot traffic and abuse. Recommended settings:

**1. Challenge Invalid Traffic (Cloudflare Setting)**
- Go to Cloudflare Dashboard → Security → WAF.
- Enable **Challenge (CAPTCHA)** rules for:
  - Known bot traffic (unless legitimately crawling, e.g., search engines).
  - High-threat traffic patterns.
- **Caution:** Do **not** overly restrict; GitHub Pages validation bots and legitimate search engine crawlers should be allowed.

**2. Allow GitHub Pages Validation**
- Cloudflare may block some traffic patterns by default. To ensure GitHub Pages health checks pass:
  - Go to Cloudflare → Firewall → Rules.
  - Add a rule: **Allow** traffic from `Cloudflare IP space` (Cloudflare's own IPs).
  - Add a rule: **Allow** traffic with User-Agent containing `github-pages` or requests from GitHub IP ranges.
  - Example rule (using IP whitelist):
    ```
    (ip.src in {140.82.112.0/21}) → Allow
    ```
    (GitHub's IP range; consult GitHub's current IP list for accuracy.)

**3. Rate Limiting (Optional)**
- Go to Cloudflare → Firewall → Rate Limiting.
- Set a threshold, e.g., 100 requests per minute from a single IP.
- Action: Challenge or Block.
- Exemption: Whitelist known good bots (Googlebot, Bingbot, etc.) to avoid blocking legitimate crawlers.

**4. Verification Steps**
- **Test legitimate visitor:** Open `https://vbzio.com` in a browser incognito window or from a different IP/device. Verify you can load the site without CAPTCHA challenges or blocks.
- **Test GitHub Pages validator:** GitHub will run health checks. If successful, GitHub will show "Your site is published at https://vbzio.com" without errors.
- **Monitor Cloudflare Analytics:** Go to Cloudflare Dashboard → Analytics. Verify that the vast majority of traffic is allowed (green), with only spam or invalid traffic challenged/blocked.
- **Search engine crawlers:** Verify in Cloudflare that Googlebot, Bingbot, and other major search crawlers are not blocked (they should show as allowed).

**Example Cloudflare Firewall Rules:**
```
# Rule 1: Allow GitHub health checks
(cf.bot_management.score lt 30) AND (http.user_agent contains "GitHub-Hookshot" OR http.user_agent contains "github-pages") → Allow

# Rule 2: Block obvious bots (with whitelist for search engines)
(cf.bot_management.score gt 70) AND NOT (cf.bot_management.verified_bots.category eq "Search Engines") → Challenge

# Rule 3: Rate limiting
(cf.threat_score gt 50) → Challenge
```

**Notes:**
- Bot Management is a paid Cloudflare feature; free tier has basic challenges and rate limiting.
- Adjust thresholds based on observed traffic patterns (start conservative, relax if legitimate traffic is blocked).
- Always test rules before deploying to production (use Cloudflare's "Simulate" or test from an incognito window).

#### 1.8 Explicit Statements on Manual Operations and Security

Add a clear section to the README:

> **Important: Manual Operator Configuration**
> 
> The following operations are **not** automated and require manual human action:
> - DNS configuration in Cloudflare or your domain registrar.
> - GitHub Pages custom domain settings.
> - SSL/TLS certificate provisioning (though GitHub automates this once DNS is correct).
> - Cloudflare bot-protection and firewall rules.
> - Domain registration and registrar account access.
> 
> This repository **contains no secrets, credentials, or API tokens**. All configuration is documented as plaintext instructions; no PI developer or tool should attempt to automate external service changes.
> 
> **Secrets Management:**
> - Never commit Cloudflare API tokens, GitHub tokens, or registrar credentials to this repository.
> - If environment variables or configuration files are needed in the future, use `.gitignore` to exclude them and document their purpose clearly.

---

### Task 2: Create or Update CNAME File (Optional but Recommended)

**File:** `CNAME` (at repository root)

**Content:**
```
vbzio.com
```

**Purpose:**
- Signals GitHub Pages that this repo is configured for the custom domain `vbzio.com`.
- Does not automatically route traffic; requires DNS configuration and Pages settings.
- Human must still complete custom domain setup in GitHub Pages settings.

**Note in README:** Include a note that `CNAME` file exists for reference but does not activate custom domain on its own.

---

### Task 3: Distinguish Required vs. Optional Recommendations

**Required:**
- Enable GitHub Pages in repository settings (on branch main, root folder).
- Add A records for GitHub Pages IPs to Cloudflare DNS (or registrar).
- Configure GitHub Pages custom domain setting (enter `vbzio.com`).
- Wait for GitHub to provision HTTPS certificate.
- Enable Enforce HTTPS in GitHub Pages settings.

**Optional (but recommended for production):**
- Add www CNAME record for `www.vbzio.com`.
- Enable Cloudflare proxy (orange cloud) after certificate is ready.
- Implement Cloudflare bot-protection and firewall rules.
- Set up Cloudflare SSL/TLS Full mode.
- Implement rate limiting on Cloudflare.

**In the README:** Use clear labels (e.g., "**Required:**" vs. "**Optional:**") to guide operators on which steps are mandatory and which are nice-to-have.

---

### Task 4: Ensure Paths and Commands Match Implementation

**Validation:**
- `python3 validate_links.py` — actual script in repo root; instructions must match.
- `python3 -m http.server 8000` — standard Python library; should work on all systems.
- File paths: `index.html`, `contact.html`, `404.html`, `style.css` all at repo root; CNAME at root.
- GitHub Pages preview URL: `https://vbz0vader-agent.github.io/vbzio/` (confirm org/user is `vbz0vader-agent`, repo is `vbzio`).
- Custom domain: `vbzio.com` (confirmed in specification and brief).

---

## Definition of Done for Issue #5

| Requirement | Status | Notes |
|---|---|---|
| README.md updated with site purpose and locked stack | ⏳ To do | Plain HTML/CSS, GitHub Pages, Cloudflare, no framework |
| Repository structure documented | ⏳ To do | List key files with descriptions |
| Local preview instructions included | ⏳ To do | `python3 -m http.server 8000` and verification steps |
| Validation instructions included | ⏳ To do | `python3 validate_links.py` and explanation |
| GitHub Pages publication steps documented | ⏳ To do | Settings, branch, expected preview URL |
| Custom domain setup for vbzio.com documented | ⏳ To do | CNAME file, Pages settings, safe order of operations |
| Cloudflare DNS records documented | ⏳ To do | A records, www CNAME, TTL, proxy status |
| SSL/TLS considerations documented | ⏳ To do | GitHub cert, Cloudflare Full SSL, safe provisioning order |
| Recommended bot-protection rules documented | ⏳ To do | Examples, verification, whitelist for validation bots |
| Clear statement on manual steps and no secrets | ⏳ To do | Explicit warning that DNS/Cloudflare are human-applied |
| Required vs. optional recommendations distinguished | ⏳ To do | Clear labels in README |
| Paths and commands match implementation | ⏳ To do | Validation against actual files and URLs |
| CNAME file created (optional but recommended) | ⏳ To do | Content: `vbzio.com` |
| docs/tasks/5-plan.md completed | ⏳ To do | This document |
| docs/tasks/5-walkthrough.md completed | ⏳ To do | Implementation narrative |

---

## Files to Modify / Create

| File | Action | Notes |
|---|---|---|
| `README.md` | Update/rewrite | Replace minimal version with comprehensive docs |
| `CNAME` | Create | Single line: `vbzio.com` |
| `docs/tasks/5-plan.md` | Create | This plan (implementation guide) |
| `docs/tasks/5-walkthrough.md` | Create | Implementation narrative (post-implementation) |

---

## Dependencies and Assumptions

- **GitHub Repository:** Already created and accessible at `https://github.com/vbz0vader-agent/vbzio`.
- **GitHub Pages:** Must be enabled in repository settings by human.
- **Cloudflare Account:** Must be set up and domain registered by human.
- **Domain Registrar:** Human has access to registrar or nameserver settings to point to Cloudflare.
- **Branch:** Work is on `feat/landing-page` branch; final branch (main or other) is determined by human operator.

---

## Next Steps

1. Read and understand the parent specification (docs/tasks/1-spec.md).
2. Implement README.md with all sections documented above.
3. Create CNAME file with content `vbzio.com`.
4. Write docs/tasks/5-walkthrough.md documenting the implementation.
5. Validate that all file paths, commands, and URLs are correct.
6. Ensure no secrets or credentials are included.
7. Submit branch for review per Loop Engineering Playbook workflow.

---

## Notes

- All external configuration (GitHub, DNS, Cloudflare) is documented as plaintext guidance for human operators.
- No secrets belong in the repository.
- The CNAME file is informational; GitHub Pages custom domain setting is what activates it.
- Safe order of operations is critical to avoid downtime or certificate errors; document clearly in README.
- Distinguish required from optional to prevent operator confusion.
- Test locally with `python3 -m http.server` and `python3 validate_links.py` before publishing.
