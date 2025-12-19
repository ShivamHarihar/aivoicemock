# Initial Project Analysis

## Architecture
- **Root**: `d:\newSamproProject\sampro-ai-interview`
- **Backend**: Flask (Python) serving API and static files.
- **Frontend**: Static HTML/JS/CSS served by Flask. No build step detected (no `package.json` build scripts).
- **Template Engine**: Currently uses `markdown2` to convert Markdown to HTML, then wraps in a basic HTML skeleton. CSS is loaded and injected.
- **PDF Generation**: `backend/src/pdf_generator.py` uses `weasyprint` (primary) and `reportlab` (fallback).
- **Data Flow**: User uploads resume -> Parsed to text -> Analyzed/Recreated by AI -> Markdown -> PDF/DOCX Export.

## Template Locations
- Existing templates: `backend/templates/`
- Configuration: `backend/templates/templates.json`
- CSS: `backend/templates/css/`
- Previews: `backend/templates/previews/`

## Export Mechanism
- **PDF**: `backend/src/pdf_generator.py`
    - `markdown_to_pdf(markdown_text, template_id)`
    - Converts Markdown to HTML.
    - Loads CSS from `backend/templates/css/{template_id}.css`.
    - Uses `weasyprint.HTML(...).write_pdf(...)`.
- **DOCX**: `backend/src/docx_generator.py` (uses `python-docx`).

## Build/Test Commands
- **Python**: `python app.py` to run.
- **Tests**: `tests/` directory exists. `scripts/test_*.py` exist.
- **Linting**: No explicit linter config found, but standard Python tools (`flake8`, `pylint`) likely applicable.

## Recommended Order of Operations
1.  **Refactor HTML Generation**: Modify `pdf_generator.py` to produce structured HTML (wrapping sections in `<div>` or `<section>`) to enable CSS Grid layouts without changing content order.
2.  **Create Template Structure**: Create `backend/templates/template-{1..5}/` with `styles.css` and `print.css`.
3.  **Implement Templates**: Write CSS for each template matching the references.
4.  **Update Export Logic**: Ensure `pdf_generator.py` loads the correct CSS files from the new structure.
5.  **Frontend Integration**: Update `ats_dashboard.html` / `template_selector.html` to allow selecting the new templates.
6.  **Verification**: Generate exports and verify against requirements.

## Files Likely to Change
- `backend/src/pdf_generator.py`
- `backend/templates/templates.json`
- `backend/app/app.py` (to expose new templates if needed)
- `frontend/public/js/ats_dashboard.js` (to handle new template selection)
- New files in `backend/templates/template-{1..5}/`
