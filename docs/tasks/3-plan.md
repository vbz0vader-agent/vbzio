# Issue #3 Implementation Plan: Scaffold GitHub Pages Static Site

## 1. Choose Site Root
The site will be served from the repository root. This means `index.html`, `404.html`, and `style.css` will reside directly in the root directory of the repository.

## 2. `index.html` Creation
*   Create a basic HTML5 structure.
*   Include a `<head>` section with:
    *   `<meta charset="UTF-8">`
    *   `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
    *   `<title>vbzio - Data Engineering & Analytics</title>` (Placeholder, will be refined later)
    *   `<meta name="description" content="vbzio offers expertise in data engineering, warehousing, ETL, Python, Airflow, dbt, SQL, and reporting.">` (Placeholder for required metadata)
    *   Link to `style.css`: `<link rel="stylesheet" href="style.css">`
*   Include a `<body>` section with:
    *   A simple header (e.g., `<h1>Welcome to vbzio</h1>`).
    *   Placeholder navigation.
    *   Placeholder content (e.g., a `<p>` tag).
    *   A basic footer.

## 3. `404.html` Creation
*   Create a basic HTML5 structure, similar to `index.html`.
*   Include the same `<head>` elements (charset, viewport, title, description, style.css link). The title will be "Page Not Found".
*   Include a `<body>` section with:
    *   A clear "404 - Page Not Found" message.
    *   A link back to the homepage: `<p>Go back to <a href="/">homepage</a>.</p>`.

## 4. `style.css` Creation
*   Create `style.css` in the repository root.
*   Define basic styles for a light theme:
    *   `body`: font-family, line-height, margin, background-color (light), color (dark).
    *   `a`: color, text-decoration.
    *   Basic responsive considerations:
        *   `max-width` for content containers.
        *   Simple media query for smaller screens if needed (e.g., adjusting padding/margin).

## 5. Validation Script (`validate_links.py`)
*   Create `validate_links.py` in the repository root.
*   **Purpose**: Verify local links and required page metadata.
*   **Requirements**: Python standard library only, no external dependencies.
*   **Functionality**:
    1.  **File Discovery**: Use `os` module to find all `.html` files in the current directory (repository root).
    2.  **HTML Parsing**: For each `.html` file:
        *   Read the file content.
        *   Use `html.parser` (or simple string/regex matching if `html.parser` is overkill for this scope) to find:
            *   All `<a>` tags with `href` attributes.
            *   The `<title>` tag content.
            *   The `<meta name="description">` tag content.
    3.  **Link Validation**:
        *   For each `href`:
            *   If it's a local path (starts with `/` or relative path, and ends with `.html` or is a directory), check if the target file/directory exists.
            *   Special handling for `/` (root) to point to `index.html`.
    4.  **Metadata Validation**:
        *   Check if a `<title>` tag is present and not empty.
        *   Check if a `<meta name="description">` tag is present and its `content` attribute is not empty.
    5.  **Reporting**: Print clear messages for broken links or missing metadata.

## Definition of Done for Issue #3
*   `index.html` exists in the repository root with basic structure, title, description meta, and CSS link.
*   `404.html` exists in the repository root with basic structure, "Page Not Found" message, and link to homepage.
*   `style.css` exists in the repository root with basic light theme styling and responsive considerations.
*   `validate_links.py` exists in the repository root and correctly identifies broken local links and missing metadata (`title`, `description`).
*   All scaffolded HTML files pass validation.
