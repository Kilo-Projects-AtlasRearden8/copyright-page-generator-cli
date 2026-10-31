# STATUS

## What was built

`copyright-page-generator-cli` — a local-first Python CLI (v0.1.0) that generates book copyright
pages with year, rights holder, ISBN, and edition from local JSON templates, exporting Markdown or
PDF.

- `copyright_page/cli.py` — argparse CLI: `generate` and `list-templates`
- `copyright_page/generator.py` — renders `{year}`, `{rights_holder}`, `{isbn}`, `{edition}`
  placeholders from JSON templates; validates required values
- `copyright_page/templates.py` — loads/validates local JSON templates
- `copyright_page/pdf_export.py` — reportlab-based PDF export
- `copyright_page/templates/default.json` — built-in KDP-style default template
- `tests/test_rendering.py` — rendering, validation, PDF header, and CLI tests (8 tests)
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — beginner-friendly usage docs, credits Asdale Dynamics, LLC
- `pyproject.toml` — package config with `copyright-page` console script
- `.gitignore` — excludes venv, caches, build artifacts, PDFs

## How to run

```bash
# install (recommended: virtual environment)
python3 -m venv .venv --system-site-packages
.venv/bin/pip install -e .

# Markdown to stdout
.venv/bin/copyright-page generate --year 2026 --rights-holder "Asdale Dynamics, LLC" \
  --isbn 978-0-000-00000-0 --edition "First Edition"

# Markdown to file
... --output copyright.md

# PDF
... --format pdf --output copyright.pdf

# list templates
.venv/bin/copyright-page list-templates

# tests
.venv/bin/python -m pytest
```

## Verification results

- `pip install -e .`: success (builds and installs cleanly)
- `pytest`: 8 passed, 0 failed
  - default template renders all four fields
  - missing required value raises RenderError
  - unknown template raises TemplateError
  - list-templates includes `default`
  - PDF export starts with `%PDF` header
  - CLI `list-templates` runs and returns exit 0
  - CLI `generate` Markdown to stdout contains all fields
  - CLI `generate` PDF to file produces a valid `%PDF` file
- Manual smoke test: Markdown stdout and PDF file output both verified

## Known gaps

- PDF rendering is a plain-text layout (light Markdown flattening only; no rich typography)
- Only one built-in template (`default`); custom templates are added to the templates dir
- No configuration file; all values supplied via CLI flags
- `.venv/`, caches, and build artifacts are gitignored and not committed
