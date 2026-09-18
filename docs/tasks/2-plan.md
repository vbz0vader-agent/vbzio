# Issue #2 Implementation Plan: Build Homepage One-Pager Sections

**Issue:** Issue #2 (homepage one-pager sections)  
**Parent:** [Issue #1 — Landing page for vbzio.com](../1-spec.md)  
**Status:** Planning  

## Overview

This plan outlines how to replace the placeholder homepage content in `index.html` with a responsive one-pager containing five distinct, navigable sections. The sections will be logically ordered, keyboard-accessible, and styled consistently with the existing light theme defined in `style.css`.

## Homepage Sections

The homepage will contain these five sections in order:

### 1. Hero Section
- **Purpose:** Identify vbzio as a solo data consulting firm and state the practical client outcome.
- **Copy:** Concise positioning statement. No invented clients, metrics, or testimonials.
- **HTML:** Use semantic `<section>` with a heading (`<h2>`) and descriptive paragraphs.
- **Styling:** Eye-catching but understated; larger typography; ample padding.
- **Navigation:** Anchor link: `#hero`

### 2. Services Section
- **Purpose:** Cover data engineering, ETL/data pipelines, data warehousing, and reporting.
- **Copy:** List and briefly describe each service.
- **HTML:** Use semantic `<section>` with heading and list structure (possibly `<ul>` or individual blocks).
- **Styling:** Clear visual hierarchy; possibly use small cards or list items for readability.
- **Navigation:** Anchor link: `#services`

### 3. Skills Section
- **Purpose:** Group relevant capabilities clearly: Python, Airflow, dbt (lowercase), SQL, and higher-level categories (data engineering, warehousing, ETL, reporting).
- **Copy:** Organized list or grouped display of tools and categories.
- **HTML:** Use semantic `<section>` with heading and grouped structure (e.g., `<ul>`, or `<div>` groups with subheadings).
- **Styling:** Clear grouping; consistent typography.
- **Navigation:** Anchor link: `#skills`

### 4. About Section
- **Purpose:** State plainly that vbzio is a one-person company available as a contractor or consultant.
- **Copy:** Concise statement about company size and availability.
- **HTML:** Use semantic `<section>` with heading and paragraph(s).
- **Styling:** Consistent with other sections.
- **Navigation:** Anchor link: `#about`

### 5. Call to Action (CTA) Section
- **Purpose:** Direct visitors to the contact page.
- **Copy:** Brief call-to-action copy with a link to `contact.html`.
- **HTML:** Use semantic `<section>` with heading and a prominent `<a>` link.
- **Link:** `href="contact.html"` (relative path; validation will use a placeholder contact.html stub).
- **Styling:** Make the link visually distinct (e.g., button-like styling with contrast).
- **Navigation:** Anchor link: `#cta`

## Navigation Structure

The site navigation will support:
- **Header nav:** Links to "Home" (`/`) and "Contact" (`contact.html`).
- **In-page anchors:** Navigation may optionally include a "Skip to section" or "Back to top" mechanism, but at minimum, all sections must be navigable via manual anchor links.
- **Focus states:** All links must have visible `:focus` styles for keyboard accessibility.

## HTML Approach

1. **Site Shell:** Keep the existing header and footer structure. Update header nav to include Contact link (initially to a placeholder `contact.html`).
2. **Main Content:** Replace the placeholder `<main>` content with five semantic `<section>` elements, each with:
   - A unique `id` for anchor navigation.
   - A descriptive `<h2>` heading.
   - Appropriate child elements (paragraphs, lists, etc.).
3. **Headings:** Maintain logical heading order: `<h1>` in header, `<h2>` for section headings, `<h3>` for subsections if needed.
4. **Semantic HTML:** Use `<section>`, `<ul>`, `<li>`, `<article>` as appropriate for content structure.

## CSS Strategy

**Update `style.css` to:**

1. **Section Styling:**
   - Add `section` styles with appropriate padding, margin, and background colors (alternate or consistent).
   - Ensure sections have sufficient breathing room.
   - Consider subtle background color variation to visually distinguish sections (light gray / white alternation).

2. **Typography:**
   - Improve typography hierarchy: larger fonts for section headings, consistent line heights.
   - Ensure readable font sizes at 320px viewport width.

3. **Interactive Elements:**
   - Style `:hover` and `:focus` states for links with clear visual feedback.
   - Ensure focus ring is visible (e.g., `outline`, `box-shadow`).

4. **Responsive Layout:**
   - Sections should stack vertically on small screens (320px–600px).
   - Maintain padding and margin proportions for readability.
   - Test that content reflows without horizontal scrolling.

5. **Color Contrast:**
   - Verify all text-to-background contrast meets WCAG 2.1 AA (≥4.5:1 for normal text, ≥3:1 for large text).
   - Ensure focus styles use sufficient contrast.

6. **Shared Shell:**
   - Keep header and footer styling consistent with existing design.
   - Ensure navigation is keyboard accessible (tab order, focus states).

## Validation Requirements

After implementation:

1. **Link Validation:** Run `python3 validate_links.py` to ensure:
   - All local links (including anchor links and `contact.html`) are valid.
   - `<title>` and `<meta description>` are present and non-empty.

2. **Contact.html Stub:** If `contact.html` does not exist, create a minimal placeholder with:
   - Proper `<title>` and `<meta description>`.
   - Header/footer matching the site shell.
   - A simple message: "Contact page coming soon" or similar.
   - A link back to `index.html`.
   - This allows validation to pass; Issue #4 will flesh out the full contact page.

3. **Manual Testing:**
   - Keyboard navigation: Tab through all links; verify focus is visible.
   - 320px viewport: Test on mobile emulator or resized browser; no horizontal scroll.
   - Color contrast: Verify all text meets WCAG 2.1 AA.
   - Semantic structure: Verify heading order is logical (no skipped levels).

## Definition of Done

- [ ] `index.html` updated with five semantic sections (Hero, Services, Skills, About, CTA).
- [ ] Each section has unique `id`, `<h2>` heading, and appropriate copy per spec.
- [ ] Sections are navigable via in-page anchors (e.g., `#hero`, `#services`).
- [ ] Header navigation includes Contact link pointing to `contact.html`.
- [ ] `style.css` updated to style sections, maintain light theme, and ensure responsive layout.
- [ ] All links have visible `:focus` styles (keyboard accessible).
- [ ] No horizontal scroll at 320px viewport.
- [ ] Color contrast meets WCAG 2.1 AA.
- [ ] Heading order is logical and semantic.
- [ ] `contact.html` stub created (if not already present) with basic shell.
- [ ] `python3 validate_links.py` returns PASSED.
- [ ] Manual testing confirms keyboard accessibility and layout.

## Files to Modify / Create

| File | Action | Notes |
|---|---|---|
| `index.html` | Modify | Replace placeholder with five sections and updated header/nav. |
| `style.css` | Modify | Add section styling, typography improvements, responsive adjustments. |
| `contact.html` | Create (if needed) | Minimal stub for validation; Issue #4 will complete. |
| `validate_links.py` | No change | Existing script will validate the updated content. |

## Next Steps

1. Implement updated `index.html` with five sections.
2. Update `style.css` with section styling and responsive adjustments.
3. Create `contact.html` stub if needed.
4. Run validation and fix any issues.
5. Manual testing (keyboard, viewport, contrast, heading order).
6. Write `2-walkthrough.md` documenting the implementation.

---

## Notes

- Copy for all sections must be factual, credible, and free of invented claims or metrics.
- Relative links (e.g., `href="contact.html"`) work at localhost preview, GitHub Pages, and custom domain.
- No external dependencies, frameworks, or build tools will be introduced.
- Styling will remain in plain CSS with no preprocessing or vendor-specific hacks.
