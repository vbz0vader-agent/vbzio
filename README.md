# vbzio

A lightweight, fast landing page for [vbzio.com](https://vbzio.com) — a one-person data consultancy.

**Identity:** All agent GitHub work under `vbz0vader-agent` (`vbz0vader@gmail.com`).

**Status:** Static site ready in-repo. GitHub Pages, custom domain, and Cloudflare bot rules are documented below and require manual human configuration (not yet claimed as live).

---

## Quick Links

- **GitHub Repository:** [vbz0vader-agent/vbzio](https://github.com/vbz0vader-agent/vbzio)
- **GitHub Pages Preview:** https://vbz0vader-agent.github.io/vbzio/
- **Custom Domain (when configured):** https://vbzio.com
- **Issue #1 Specification:** [docs/tasks/1-spec.md](docs/tasks/1-spec.md)
- **Engineering Playbook:** [docs/Loop-Engineering-Playbook.md](docs/Loop-Engineering-Playbook.md)

---

## Site Purpose and Technology Stack

**vbzio** is a one-person data consultancy landing page. The site presents services in data engineering, ETL pipelines, data warehousing, and reporting, with a direct email contact mechanism.

### Technology Choices (Locked)

- **Static HTML and CSS:** Plain, hand-authored HTML5 and CSS3. No framework, no static-site generator, no build tools, no runtime dependencies.
- **Hosting:** GitHub Pages from this repository (root folder, branch `main`).
- **Custom Domain:** `vbzio.com` via Cloudflare DNS.
- **Bot Protection:** Cloudflare firewall and optional DDoS protection (human-configured).
- **Contact:** `mailto:vbz0vader@gmail.com` only; no form backend, API, or third-party service.

**Why?**
- Fast, minimal, and maintainable for a lightweight marketing site.
- Free hosting (GitHub Pages) with automatic HTTPS.
- No secrets or credentials needed in the repository.
- Easy for non-developers to update copy without build steps.
- Reliable and performant with zero runtime complexity.

---

## Repository Structure

```
vbzio/
├── index.html              # Homepage: Hero, Services, Skills, About, CTA sections
├── contact.html            # Contact page with mailto link
├── 404.html                # Error page (GitHub Pages fallback)
├── style.css               # Shared light-theme stylesheet (responsive, accessible)
├── CNAME                   # Custom domain file (vbzio.com) — signals GitHub Pages config
├── validate_links.py       # Lightweight validation script (links, metadata)
├── README.md               # This file
└── docs/
    ├── Loop-Engineering-Playbook.md
    ├── tasks/
    │   ├── 1-spec.md       # Parent specification
    │   ├── 1-brief.md      # PO brief
    │   ├── 2-plan.md       # Homepage plan
    │   ├── 2-walkthrough.md
    │   ├── 3-plan.md       # Contact/shell plan
    │   ├── 3-walkthrough.md
    │   ├── 4-plan.md       # Styling and 404 plan
    │   ├── 4-walkthrough.md
    │   ├── 5-plan.md       # This documentation plan
    │   └── 5-walkthrough.md
    └── tasks/README.md
```

### Key Files

| File | Purpose |
|---|---|
| `index.html` | Homepage with five sections: Hero (identify vbzio and value), Services (data engineering, ETL, warehousing, reporting), Skills (Python, Airflow, dbt, SQL), About (one-person company), CTA (contact link). |
| `contact.html` | Contact page with prominent `mailto:vbz0vader@gmail.com` link and fallback email address in visible copy. |
| `404.html` | Error page served by GitHub Pages when a requested URL is not found; includes navigation back to homepage. |
| `style.css` | Light-theme stylesheet. Responsive from 320px upward. Keyboard accessible. WCAG 2.1 AA color contrast. No external fonts or dependencies. |
| `CNAME` | Single line: `vbzio.com`. Signals GitHub Pages that this repository is configured for a custom domain (does not activate on its own; requires DNS and Pages settings). |
| `validate_links.py` | Python 3 script validating all `.html` files for non-empty `<title>` and `<meta description>` tags, and checking that all internal links point to existing files. Lightweight, no dependencies. |

---

## Local Preview and Development

### Start a Local Server

To preview the site locally, run a simple HTTP server:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser. You should see the homepage styled and fully functional.

**Why this works:**
- All links use relative paths (e.g., `contact.html`, `/404.html`) or root-relative paths (e.g., `/`), so they resolve correctly at localhost.
- No build step is needed; the files are served as-is.
- Styles, links, and JavaScript (if any) load correctly from the local file paths.

### Stop the Server

Press `Ctrl+C` in the terminal where you ran `http.server`.

---

## Validation

### Link and Metadata Validation

Before committing or deploying, run the validation script to catch broken links and missing metadata:

```bash
python3 validate_links.py
```

**Expected output on success:**
```
Validation PASSED: All local links and metadata are valid.
```

**What it checks:**
- All `.html` files have a non-empty `<title>` tag.
- All `.html` files have a non-empty `<meta name="description">` tag.
- All internal local links (relative and root-relative paths) point to existing files.
- External links (http://, https://, mailto:) are not validated locally (assumed correct).

**Fix broken links:**
- If validation fails, read the error message to identify the file and link.
- Ensure relative links are spelled correctly (case-sensitive on Linux/Mac).
- Ensure target files exist (e.g., if `contact.html` is referenced, the file must exist).

**Use in CI/CD:** This script can be run in GitHub Actions or other CI systems to catch errors before merge.

---

## GitHub Pages Publication

### Prerequisites

- This repository is already set up with GitHub Pages.
- You have push access to the repository.

### Steps to Publish

#### Step 1: Enable GitHub Pages (if not already enabled)

1. Go to the repository on GitHub: https://github.com/vbz0vader-agent/vbzio
2. Click **Settings** → **Pages**.
3. Under **Source**, select:
   - **Branch:** `main` (or the branch you're deploying from)
   - **Folder:** `/ (root)`
4. Click **Save**.

#### Step 2: Wait for Initial Setup

GitHub will provision an HTTPS certificate and publish the site. This typically takes 5–10 minutes. You'll see:
- "Your site is being built" (in progress)
- "Your site is published at https://vbz0vader-agent.github.io/vbzio/" (complete)

#### Step 3: Verify the Preview URL

Visit https://vbz0vader-agent.github.io/vbzio/ in your browser. You should see:
- Homepage with Hero, Services, Skills, About, and CTA sections.
- Navigation links to Contact page.
- Proper styling and responsive layout.
- All links working correctly (including Contact page mailto link).

**Note:** This is the GitHub Pages **preview URL**. The custom domain setup (next section) makes the site available at `https://vbzio.com`.

---

## Custom Domain Setup: vbzio.com

### Overview

To serve the site at `vbzio.com` instead of the GitHub Pages preview URL, you must:
1. Configure DNS records to point `vbzio.com` to GitHub Pages.
2. Set up a custom domain in GitHub Pages settings.
3. Enable HTTPS once the certificate is provisioned.

This is a multi-step process involving external services. **No code changes are needed in this repository**, but human configuration is required.

### Step 1: CNAME File (Already in Repository)

The file `CNAME` in the repository root contains:
```
vbzio.com
```

This file **signals the intent** to GitHub Pages but does **not** activate the custom domain on its own. You must complete the DNS and GitHub settings steps below.

### Step 2: Configure DNS Records (Cloudflare or Your Registrar)

The site is configured to use **Cloudflare** for DNS and bot protection. If you are using a different registrar or DNS provider, adapt the steps accordingly.

#### Option A: Cloudflare (Recommended)

**Prerequisites:**
- Cloudflare account (sign up at https://www.cloudflare.com/).
- Domain `vbzio.com` registered and nameservers pointed to Cloudflare (if transferring from a registrar).

**Add DNS Records to Cloudflare:**

1. Log in to Cloudflare Dashboard.
2. Select the **vbzio.com** zone.
3. Go to **DNS** → **Records**.
4. Add four **A records** for GitHub Pages (these are the IP addresses of GitHub Pages servers):

   ```
   Type: A
   Name: vbzio.com (or @)
   Content: 185.199.108.153
   TTL: Auto
   Proxy status: DNS only (grey cloud icon)
   ```

   Then add three more A records with the same Name and TTL but these contents:
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`

5. (Optional) Add a CNAME record for the www subdomain:

   ```
   Type: CNAME
   Name: www
   Content: vbz0vader-agent.github.io
   TTL: Auto
   Proxy status: DNS only (grey cloud icon)
   ```

   This allows `www.vbzio.com` to resolve to the GitHub Pages preview URL (GitHub can redirect this to apex or serve it as a separate alias).

6. Click **Save** for each record.

**Proxy Status:** Initially set all records to **"DNS only" (grey cloud)**, not Cloudflare proxy (orange cloud). This is important for the next step (GitHub certificate provisioning). You can enable Cloudflare proxy later once the certificate is ready.

#### Option B: Other Registrar (Namecheap, GoDaddy, etc.)

If you're not using Cloudflare, add the same four A records through your registrar's DNS management:
- Name: `@` or `vbzio.com` (root domain)
- Type: A
- Values: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (typically one per record, or all in a single CNAME/A record depending on your registrar's UI)

Refer to your registrar's documentation for specific steps.

**DNS Propagation:** After adding records, wait 5–15 minutes for DNS to propagate globally. You can check propagation at https://www.whatsmydns.net/ by searching for `vbzio.com`.

### Step 3: Configure GitHub Pages Custom Domain Setting

Once DNS records are in place:

1. Go to the repository on GitHub: https://github.com/vbz0vader-agent/vbzio
2. Click **Settings** → **Pages**.
3. Under **Custom domain**, enter `vbzio.com` and click **Save**.
4. GitHub will validate that DNS records point to GitHub Pages. If validation succeeds, you'll see a green checkmark.
5. GitHub will automatically request an HTTPS certificate from Let's Encrypt. This takes 5–30 minutes. You'll see:
   - "Certificate is being provisioned" (in progress)
   - "Certificate issued" or "Your site is published at https://vbzio.com/" (complete)

**If validation fails:** Check that your DNS A records are correctly pointing to the four GitHub IPs listed above. Ensure "Proxy status" is set to "DNS only" in Cloudflare (or equivalent in your registrar).

### Step 4: Enable Enforce HTTPS

Once GitHub confirms the certificate is ready:

1. Go to **Settings** → **Pages**.
2. Check the box **"Enforce HTTPS"**.
3. Click **Save**.

This forces all HTTP traffic to `https://vbzio.com` (required for security and modern browser standards).

**Important:** Do not enable "Enforce HTTPS" until GitHub confirms the certificate is ready. Enabling it too early can cause temporary downtime or certificate errors.

### Step 5: Verify the Custom Domain

1. Visit https://vbzio.com in your browser.
2. You should see the homepage load correctly with full styling and navigation.
3. Click links and verify they work (Contact page, Back to Home, etc.).
4. The URL should stay at `https://vbzio.com` (no redirect to GitHub Pages preview URL).

### Safe Order of Operations Summary

To avoid downtime and certificate provisioning issues, follow this order:

1. **DNS Setup (Phase 1):** Add A records to Cloudflare or registrar pointing to GitHub IPs. Set Cloudflare proxy status to "DNS only".
2. **GitHub Certificate (Phase 2):** Configure custom domain in GitHub Pages settings. Wait for GitHub to provision the HTTPS certificate (5–30 minutes).
3. **Enforce HTTPS (Phase 3):** Once certificate is ready, enable "Enforce HTTPS" in Pages settings.
4. **Cloudflare Proxy (Phase 4, optional):** Once the site is working at https://vbzio.com, optionally enable Cloudflare proxy (orange cloud) for additional DDoS protection and bot filtering. See Cloudflare section below.

---

## Cloudflare Configuration (Optional but Recommended for Production)

### Overview

Cloudflare provides DNS hosting, DDoS protection, and bot-filtering services. This section documents recommended settings to protect the site while allowing legitimate traffic (including GitHub Pages validation and search engine crawlers).

### DNS and SSL/TLS Configuration

#### SSL/TLS Mode

Once Cloudflare proxy is enabled (Phase 4 above), set the SSL/TLS mode:

1. Go to Cloudflare Dashboard → **SSL/TLS**.
2. Under **Overview**, set **SSL/TLS encryption mode** to:
   - **Full** (recommended): Encrypts traffic from client → Cloudflare → GitHub, and Cloudflare validates GitHub's certificate.
   - **Full (strict)**: Same as Full but with stricter certificate validation.

Do **not** use "Flexible" mode, as this would encrypt client → Cloudflare only but not Cloudflare → GitHub, exposing data in transit.

#### SSL/TLS Certificates

GitHub Pages automatically issues an HTTPS certificate for your custom domain. Cloudflare will use this certificate once proxy is enabled. **No manual certificate upload is needed.**

---

### Bot Protection and Firewall Rules

Cloudflare's bot-protection features help reduce spam, DDoS, and unwanted traffic. This static site has no form backend or sensitive data, so protection is light. The goal is to prevent abuse while allowing legitimate visitors, search engines, and GitHub Pages validation.

#### Goal and Caution

- **Goal:** Reduce bot traffic and obvious abuse attempts while keeping the site accessible to legitimate visitors.
- **Caution:** Overly aggressive rules can block search engine crawlers (Google, Bing) and GitHub's own validation systems, reducing visibility and causing GitHub Pages to report errors.

#### Recommended Rules

**Rule 1: Allow GitHub Pages Validation**

GitHub Pages performs periodic health checks on your site. Cloudflare must not block these requests.

In Cloudflare Dashboard → **Firewall** → **Rules**, add:

```
(cf.bot_management.verified_bots.category eq "GitHub") → Allow
```

Or, if Bot Management is not available on your plan, whitelist GitHub's IP ranges:

```
(ip.src in {140.82.112.0/21 140.82.113.0/21 140.82.114.0/21 140.82.115.0/21}) → Allow
```

(GitHub's IP blocks; check GitHub's documentation for the most current list.)

**Rule 2: Allow Search Engine Crawlers**

Allow major search engines to crawl and index the site:

```
(cf.bot_management.verified_bots.category eq "Search Engines") → Allow
```

This whitelist includes Googlebot, Bingbot, Yahoo Slurp, and other major crawlers.

**Rule 3: Challenge Obvious Bots (If Bot Management is available)**

If your Cloudflare plan includes Bot Management, add a rule to challenge suspicious traffic:

```
(cf.bot_management.score gt 70) AND NOT (cf.bot_management.verified_bots.category eq "Search Engines") → Challenge
```

This presents a CAPTCHA to traffic with a high bot score (>70), unless it's a verified search engine.

**Rule 4: Rate Limiting (Optional)**

To prevent brute-force or flood attacks, add a simple rate limit:

Go to **Firewall** → **Rate Limiting** and add:

```
URL: *
Threshold: 100 requests per minute per IP
Action: Block
```

Adjust the threshold based on expected legitimate traffic. For a marketing site, 100 req/min per IP is generous and unlikely to affect real visitors.

#### Verification Steps

After setting up rules, verify that legitimate traffic is not blocked:

1. **Manual browser test:** Open https://vbzio.com in an incognito window or from a different device/network. You should load the page without a CAPTCHA or error.
2. **GitHub Pages validation:** Go to repository Settings → Pages and verify GitHub shows "Your site is published at https://vbzio.com/" without errors.
3. **Search engine indexing:** After a few hours/days, check Google Search Console to verify Googlebot can crawl your site without errors.
4. **Cloudflare Analytics:** Go to Cloudflare Dashboard → **Analytics**, and review traffic. Most requests should be "Allowed"; spam or obvious bots should be "Challenged" or "Blocked" in small numbers.

If you see many legitimate requests being blocked, relax the rules or add exceptions.

---

## Important: Manual Operations and No Secrets

### DNS and Cloudflare Are Manual Steps

The following operations are **not** automated and **require manual human action:**

- Domain registration and registrar account setup.
- DNS record creation and management (Cloudflare or your registrar).
- GitHub Pages custom domain setting and HTTPS enforcement.
- Cloudflare firewall rules and bot-protection configuration.
- Cloudflare proxy enablement and SSL/TLS mode selection.

**This repository contains no scripts, CI/CD workflows, or code to automate these steps.** They require human judgment and access to external accounts.

### No Secrets in Repository

- **Never commit Cloudflare API tokens, GitHub tokens, or domain registrar credentials to this repository.**
- All configuration documented in this README is plaintext guidance for human operators.
- If in the future you need to store secrets (e.g., for automated deployments), use:
  - GitHub Secrets for CI/CD workflows.
  - `.gitignore` to exclude local configuration files.
  - Separate secure storage (e.g., 1Password, Vault) for credentials accessed manually.

### Assumptions and Prerequisites

This README assumes:
- You have administrative access to the GitHub repository.
- You own or have control over the domain `vbzio.com` (or can register it).
- You have or can create a Cloudflare account (free tier available).
- You understand basic DNS and domain management concepts.

If you lack access to any of these, coordinate with the appropriate human stakeholder before proceeding.

---

## Accessibility and Quality Standards

The site meets these standards:

- **Semantic HTML:** Proper heading hierarchy, landmark roles, and descriptive link text.
- **Keyboard Navigation:** All links and buttons are reachable and operable via Tab and Enter keys.
- **Focus Indicators:** Visible yellow focus outlines (2px, 4px offset) on all interactive elements.
- **Color Contrast:** Text and backgrounds meet WCAG 2.1 AA (≥4.5:1 for normal text).
- **Responsive Design:** Layout adapts without horizontal scrolling from 320px to 1440px+ viewports.
- **Performance:** No external dependencies, minimal CSS, fast load times.
- **No Tracking:** No analytics, remote fonts, or third-party scripts.

---

## Contributing

This repository is maintained by `vbz0vader-agent`. Contributions follow the Loop Engineering Playbook workflow:

1. Read `docs/Loop-Engineering-Playbook.md`.
2. Create a feature branch (e.g., `feat/feature-name`).
3. Make changes and validate locally with `python3 validate_links.py`.
4. Open a pull request.
5. Address review feedback.
6. Merge after approval.

---

## Support and Questions

- **Issue Tracker:** https://github.com/vbz0vader-agent/vbzio/issues
- **Contact:** vbz0vader@gmail.com
- **Documentation:** See `docs/` directory for specifications, plans, and walkthroughs.

---

## License

This project is proprietary. All content, code, and branding are owned by vbz0vader.

---

## Summary

**vbzio** is a fast, simple, and maintainable landing page for a one-person data consultancy. It uses plain HTML and CSS served by GitHub Pages, with optional Cloudflare bot protection. This README provides all the guidance needed for local preview, validation, GitHub Pages publication, and custom domain setup. No code deployment or external automation is required; all external configuration is manual human steps documented clearly and without secrets.
