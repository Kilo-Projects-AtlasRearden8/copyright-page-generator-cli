"""Command-line interface for the copyright page generator."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .generator import RenderError, render
from .pdf_export import export_pdf, export_pdf_bytes
from .templates import TemplateError, list_templates, load_template


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="copyright-page",
        description="Generate book copyright pages (Markdown or PDF) from local JSON templates.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Render a copyright page to Markdown or PDF")
    gen.add_argument("--year", default=None, help="Copyright year (defaults to current year)")
    gen.add_argument("--rights-holder", required=True, help="Rights holder name")
    gen.add_argument("--isbn", required=True, help="Book ISBN")
    gen.add_argument("--edition", required=True, help="Edition statement (e.g. 'First Edition')")
    gen.add_argument("--template", default="default", help="Template name (default: 'default')")
    gen.add_argument(
        "--format", choices=["markdown", "pdf"], default="markdown", dest="fmt", help="Output format"
    )
    gen.add_argument("--output", default=None, help="Output file path (defaults to stdout)")
    gen.add_argument(
        "--templates-dir", default=None, help="Directory of JSON templates (default: built-in templates)"
    )

    sub.add_parser("list-templates", help="List available local templates").add_argument(
        "--templates-dir", default=None, help="Directory of JSON templates (default: built-in templates)"
    )

    return parser


def cmd_generate(args: argparse.Namespace) -> int:
    import datetime

    context = {
        "year": args.year or str(datetime.date.today().year),
        "rights_holder": args.rights_holder,
        "isbn": args.isbn,
        "edition": args.edition,
    }
    try:
        markdown_text = render(context, template_name=args.template, templates_dir=args.templates_dir)
    except (RenderError, TemplateError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.fmt == "markdown":
        content = markdown_text
        target: Optional[str] = args.output
        if target:
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(content if content.endswith("\n") else content + "\n")
        else:
            sys.stdout.write(content if content.endswith("\n") else content + "\n")
        return 0

    try:
        pdf_bytes = export_pdf_bytes(markdown_text)
    except Exception as exc:  # reportlab errors surface at render time
        print(f"error: failed to build PDF: {exc}", file=sys.stderr)
        return 1
    target = args.output
    if target:
        with open(target, "wb") as handle:
            handle.write(pdf_bytes)
    else:
        sys.stdout.buffer.write(pdf_bytes)
    return 0


def cmd_list_templates(args: argparse.Namespace) -> int:
    try:
        templates = list_templates(args.templates_dir)
    except TemplateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not templates:
        print("No templates found.")
        return 0
    for entry in templates:
        desc = f" - {entry['description']}" if entry["description"] else ""
        print(f"{entry['name']}{desc}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "list-templates":
        return cmd_list_templates(args)
    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
