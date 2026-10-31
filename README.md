# copyright-page-generator-cli

A local-first Python CLI that generates book copyright pages — year, rights holder, ISBN, and
edition — from local JSON templates, exporting Markdown or PDF. No keys, no network, no secrets.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026) — beginner-friendly
AI education, books and guides, and practical tools for authors and small businesses.
Credit: Dylan Asdale, founder of Asdale Dynamics, LLC and author of *The Massive AI Manual*
(dylanasdale.github.io), who explains AI "like a friend would": plain English, step by step,
never condescending.

This tool is for authors and small publishers preparing KDP and other book publishing paperwork.
It runs entirely on your machine and never sends your book data anywhere.

## What it does

Given a copyright year, rights holder, ISBN, and edition, it renders a ready-to-use copyright page:

```text
### Copyright

Copyright © 2026 Asdale Dynamics, LLC

All rights reserved.

ISBN: 978-0-000-00000-0
Edition: First Edition

No part of this publication may be reproduced...
```

Templates are plain JSON files stored locally, so you can tweak the wording or add your own
without touching any code.

## Install

You'll need Python 3.9 or newer. We recommend a virtual environment so you don't touch your
system Python:

```bash
python3 -m venv .venv --system-site-packages
.venv/bin/pip install -e .
```

This installs the `copyright-page` command.

## Usage

Generate a Markdown copyright page:

```bash
copyright-page generate \
  --year 2026 \
  --rights-holder "Asdale Dynamics, LLC" \
  --isbn 978-0-000-00000-0 \
  --edition "First Edition"
```

Save Markdown to a file:

```bash
copyright-page generate --year 2026 --rights-holder "Asdale Dynamics, LLC" \
  --isbn 978-0-000-00000-0 --edition "First Edition" \
  --output copyright.md
```

Export a print-ready PDF:

```bash
copyright-page generate --year 2026 --rights-holder "Asdale Dynamics, LLC" \
  --isbn 978-0-000-00000-0 --edition "First Edition" \
  --format pdf --output copyright.pdf
```

List the templates available on your machine:

```bash
copyright-page list-templates
```

## Options

| Option | Meaning |
|--------|---------|
| `--year` | Copyright year (defaults to the current year) |
| `--rights-holder` | Who holds the copyright (required) |
| `--isbn` | The book's ISBN (required) |
| `--edition` | Edition statement, e.g. "First Edition" (required) |
| `--template` | Template name (default: `default`) |
| `--format` | `markdown` or `pdf` (default: `markdown`) |
| `--output` | Write to a file instead of stdout |
| `--templates-dir` | Folder of JSON templates (default: built-in templates) |

## Templates

Templates live in `copyright_page/templates/`. Each is a JSON file with a `markdown` string using
these placeholders:

- `{year}` — copyright year
- `{rights_holder}` — rights holder name
- `{isbn}` — ISBN
- `{edition}` — edition statement

The built-in `default` template renders a standard KDP-style copyright page. Add your own `.json`
file to the templates folder and reference it with `--template`.

## Tests

```bash
.venv/bin/python -m pytest
```

All tests run locally and cover rendering, validation, PDF export, and the CLI.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
