# copyright-page-generator-cli

Local-first Python CLI that generates book copyright pages (year, rights holder, ISBN, edition)
from local JSON templates, exporting Markdown or PDF. No keys, no network, no secrets.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026) — beginner-friendly
AI education, books and guides, and practical tools for authors and small businesses.
Credit: Dylan Asdale, founder of Asdale Dynamics, LLC and author of *The Massive AI Manual*
(dylanasdale.github.io).

## Install

```bash
pip install .
```

Or run from source:

```bash
pip install -e .
```

## Usage

```bash
copyright-page generate \
  --year 2026 \
  --rights-holder "Asdale Dynamics, LLC" \
  --isbn 978-0-578-00000-0 \
  --edition "First Edition"
```

Write Markdown to a file:

```bash
copyright-page generate --year 2026 --rights-holder "Your Name" \
  --isbn 978-0-000-00000-0 --edition "First Edition" --output copyright.md
```

Export a print-ready PDF:

```bash
copyright-page generate --year 2026 --rights-holder "Your Name" \
  --isbn 978-0-000-00000-0 --edition "First Edition" \
  --format pdf --output copyright.pdf
```

List available local templates:

```bash
copyright-page list-templates
```

## Templates

Templates are local JSON files in `copyright_page/templates/`. The built-in `default` template
renders a standard KDP-style copyright page with `{year}`, `{rights_holder}`, `{isbn}`, and
`{edition}` placeholders. Add your own template JSON to the directory and pass it with `--template`.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
