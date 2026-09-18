# Issue #4 Plan — Add contact mailto page

**Parent issue:** [#1 — Landing page for vbzio.com (Loop dry-run #1)](https://github.com/vbz0vader-agent/vbzio/issues/1)  
**Child issue:** Issue #4  
**Audience:** Pi Coder  
**Status:** Planning  
**Stack:** Plain HTML/CSS, mailto: link to `vbz0vader@gmail.com`

## Goal

Expand the minimal contact.html stub (from Issue #2) into a full, production-ready contact page that meets the DoD while maintaining consistency with the homepage, 404 page, and site shell.

## Current state

- `contact.html` exists with basic structure: header, title, meta description, single section with a mailto: link, and footer.
- The page follows the site's light responsive shell.
- `index.html` and `404.html` share the same header/footer/nav pattern.
- `style.css` provides responsive design down to 320px.
- `validate_links.py` checks for broken internal links and metadata (title + meta description).

## Work to complete

### 1. Enhance contact.html

The existing contact.html is nearly complete but can be polished:

- **Copy refinement:** Ensure the contact copy is concise, clear, and professional. Current copy is acceptable but could emphasize the direct contact path.
- **Email visibility:** The email address (`vbz0vader@gmail.com`) is currently visible only inside the mailto: link text. Keep it visible as text to serve as a fallback (already done in current version; confirm in final review).
- **Subject prefill:** The `mailto:` link currently uses no subject. Optionally add a URL-encoded subject like `subject=vbzio%20inquiry` for better UX, but this is not required by DoD.
- **Structure and accessibility:** Confirm semantic HTML, heading hierarchy, keyboard navigation, focus indicators, and color contrast.
- **Responsive layout:** Verify layout at 320px, 600px, 768px, and desktop widths using the existing CSS.

### 2. Validate consistency across shell pages

Ensure all three main pages (index.html, contact.html, 404.html) share:

- Same header structure and navigation.
- Same footer structure and copyright notice.
- Consistent section padding and styling.
- Proper use of `style.css` classes.
- Matching alt text conventions (if any images are added in future work).

### 3. Run link and metadata validation

Execute `python3 validate_links.py` to confirm:

- All internal links resolve correctly (contact.html links to /, / links to contact.html).
- Title and meta description are present and non-empty on contact.html.
- No broken links in index.html or 404.html.

### 4. Manual accessibility check

Test contact.html for:

- Keyboard navigation (Tab, Shift+Tab, Enter on links).
- Focus visibility on nav and CTA links (visible outline).
- Color contrast between text and background (should meet WCAG 2.1 AA).
- Viewport rendering at 320px without horizontal scroll.
- Semantic structure (header, nav, main, footer landmarks).

### 5. Documentation

Create `docs/tasks/4-walkthrough.md` summarizing:

- Changes made to contact.html (if any).
- Validation results.
- Accessibility and responsive testing results.
- Confirmation that DoD is met.

## Definition of Done

- [ ] contact.html contains concise contact copy and a prominent `mailto:vbz0vader@gmail.com` link.
- [ ] Email address is visible as fallback text in the page copy.
- [ ] contact.html shares the same header/footer/nav/styling as index.html and 404.html.
- [ ] Title tag and meta description are present and meaningful.
- [ ] `python3 validate_links.py` exits with code 0 (PASS).
- [ ] Keyboard navigation, focus visibility, and 320px layout work correctly.
- [ ] No form, backend, CAPTCHA, Turnstile, or third-party service.
- [ ] docs/tasks/4-walkthrough.md documents the work and validation.

## Constraints

- Plain HTML/CSS only; no JavaScript, form backend, or external services.
- No secrets printed to console or committed to repository.
- Use relative or root-relative links that work at GitHub Pages preview URL and vbzio.com.
- Maintain existing style.css (no modifications needed for contact page to work).

## Acceptance criteria

1. contact.html renders correctly across viewport widths (320px–desktop).
2. All internal links are valid and keyboard-navigable.
3. Page is fully accessible (WCAG 2.1 AA).
4. validate_links.py returns 0.
5. Walkthrough documents all testing and confirms DoD.
