# Issue #1 Specification — vbzio.com Landing Page

**Parent issue:** [#1 — Landing page for vbzio.com (Loop dry-run #1)](https://github.com/vbz0vader-agent/vbzio/issues/1)  
**Audience:** Pi Coder  
**Status:** Specced  
**Stack:** GitHub Pages, plain HTML/CSS, Cloudflare, `mailto:vbz0vader@gmail.com`

## Goal

Publish a fast, accessible, light-theme marketing site for vbzio.com that presents vbzio as a one-person data consultancy and gives prospective clients a direct email contact path.

## Delivery boundaries

- Use plain, hand-authored HTML and CSS served by GitHub Pages. Do not add a static-site generator, JavaScript framework, build pipeline, package manager, or runtime dependency.
- Keep the site static. The only contact mechanism is a `mailto:` link to `vbz0vader@gmail.com`; no data is submitted to or stored by the site.
- Keep all GitHub Pages source in the repository layout selected by the scaffold child issue. Later child issues must build on that layout rather than create a second site root.
- Use semantic HTML, responsive CSS, and a light, modern visual treatment.
- Human operators configure GitHub Pages and Cloudflare. Repository work may document those settings but must not require Cloudflare credentials or attempt live DNS/rules changes.

## Functional requirements

### 1. GitHub Pages scaffold

- Provide a deployable static-site entry point at `/`.
- Provide shared styling that supports both the homepage and contact page.
- Use relative or root-relative internal links that work at the GitHub Pages preview URL and at the vbzio.com custom domain.
- Include a repository `404.html` suitable for GitHub Pages; it may reuse the site shell and must provide a route back home.
- Add a lightweight automated validation command or script that catches broken local links and missing required page metadata without introducing a production runtime dependency.

### 2. Homepage

The homepage must contain these distinct, navigable sections:

1. **Hero:** identify vbzio as solo data consulting and state the practical client outcome.
2. **Services:** cover data engineering, ETL/data pipelines, data warehousing, and reporting.
3. **Skills:** group relevant capabilities clearly, including Python, Airflow, dbt, and SQL. Use the official lowercase spelling `dbt`.
4. **About:** state plainly that vbzio is a one-person company available as a contractor or consultant.
5. **Call to action:** direct visitors to the contact page.

Copy must be concise, credible, and free of unsupported claims, invented client names, testimonials, certifications, metrics, or case studies.

### 3. Contact page

- Provide a dedicated contact page linked from the homepage and site navigation.
- Include short contact copy and a prominent `mailto:vbz0vader@gmail.com` action.
- A URL-encoded subject prefill is allowed, but the recipient address must remain visible in page copy as a fallback.
- Do not include a form, client-side submission code, CAPTCHA, Turnstile, scheduling widget, or third-party contact service.

### 4. Repository and operator documentation

Update the README with:

- the site's purpose and locked technology choices;
- repository structure and local preview/validation instructions;
- GitHub Pages publication steps and expected preview URL;
- custom-domain setup for `vbzio.com`, including the repository custom-domain setting or `CNAME` file as applicable;
- Cloudflare DNS records needed for apex and optional `www`, SSL/TLS considerations, and a safe order of operations for GitHub certificate provisioning and Cloudflare proxying;
- recommended Cloudflare bot-protection/rules configuration for this static site, including what the human should verify to avoid blocking GitHub Pages validation or ordinary visitors;
- a clear statement that DNS and Cloudflare changes are manual operator steps and that no secrets belong in the repository.

Documentation must distinguish required settings from optional recommendations and must not claim that DNS, TLS, or bot rules have been applied unless a human verifies them.

## Quality requirements

- Pages must remain usable at viewport widths from 320px upward without horizontal scrolling.
- Navigation, calls to action, and email links must be keyboard accessible with visible focus states.
- Use semantic landmarks, a logical heading order, descriptive link text, meaningful page titles, and useful meta descriptions.
- Text and interactive controls must meet WCAG 2.1 AA color-contrast targets.
- Images are optional. Any informative image must have meaningful alternative text; decorative images must use empty alternative text.
- Do not load tracking, analytics, remote fonts, or other unnecessary third-party assets.
- Avoid committing credentials, API tokens, generated dependency trees, or vendored frameworks.
- Current versions of Chrome, Firefox, and Safari should render the content and navigation correctly.

## Out of scope

- Form backend or contact API
- Cloudflare Turnstile
- Blog, CMS, authentication, payments, or analytics
- Dark mode
- JavaScript framework or static-site generator
- Live GitHub Pages, DNS, registrar, SSL/TLS, or Cloudflare account changes by Pi
- Branding work beyond a simple text treatment and light static presentation

## Work breakdown and dependencies

1. Scaffold GitHub Pages static site.
2. Build homepage one-pager sections on the scaffold.
3. Add the contact mailto page using the shared site shell.
4. Complete README and Cloudflare DNS/bot-rules documentation after the final repository layout is known.

Each child issue must stay within its boundary, reference this specification and parent issue, and leave the repository in a reviewable state. Dependencies may be implemented sequentially or in one coordinated branch, but acceptance must be reportable per child.

## Definition of Done

- [ ] A plain HTML/CSS site is available through the repository's GitHub Pages preview URL.
- [ ] `/` contains Hero, Services, Skills, About, and Contact CTA sections with the required positioning and factual copy.
- [ ] A dedicated contact page contains a working `mailto:vbz0vader@gmail.com` link and visible fallback address.
- [ ] Homepage, contact page, and 404 page share a coherent light, responsive presentation.
- [ ] Internal navigation and required metadata pass the repository's documented validation command.
- [ ] Keyboard navigation, visible focus, semantic structure, contrast, and 320px layout have been manually checked.
- [ ] No form backend, Turnstile, framework, generator, analytics, or other out-of-scope feature is present.
- [ ] README documents local preview, validation, GitHub Pages publishing, vbzio.com custom-domain setup, and Cloudflare DNS/SSL/bot-rule guidance.
- [ ] README clearly marks Cloudflare and DNS operations as human-applied and contains no secrets.
- [ ] All four child issues are complete and their implementation is summarized in `docs/tasks/1-walkthrough.md`.
- [ ] The implementation is submitted for Tech Lead review with the workflow state required by the Loop Engineering Playbook.
