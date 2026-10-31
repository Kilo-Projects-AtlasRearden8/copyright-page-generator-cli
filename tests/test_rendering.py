"""Tests for copyright page rendering and export."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from copyright_page.generator import RenderError, render
from copyright_page.pdf_export import export_pdf_bytes
from copyright_page.templates import TemplateError, list_templates, load_template


def test_default_template_renders_all_fields():
    output = render(
        {
            "year": "2026",
            "rights_holder": "Asdale Dynamics, LLC",
            "isbn": "978-0-578-00000-0",
            "edition": "First Edition",
        }
    )
    assert "2026" in output
    assert "Asdale Dynamics, LLC" in output
    assert "978-0-578-00000-0" in output
    assert "First Edition" in output
    assert output.startswith("### Copyright")


def test_missing_required_value_raises():
    with pytest.raises(RenderError):
        render(
            {
                "year": "2026",
                "rights_holder": "Asdale Dynamics, LLC",
                "isbn": "978-0-578-00000-0",
            }
        )


def test_unknown_template_raises():
    with pytest.raises(TemplateError):
        load_template("does-not-exist")


def test_list_templates_contains_default():
    templates = list_templates()
    names = [entry["name"] for entry in templates]
    assert "default" in names


def test_pdf_export_starts_with_pdf_header():
    output = render(
        {
            "year": "2026",
            "rights_holder": "Asdale Dynamics, LLC",
            "isbn": "978-0-578-00000-0",
            "edition": "First Edition",
        }
    )
    pdf = export_pdf_bytes(output)
    assert pdf.startswith(b"%PDF")


def test_cli_list_templates_runs():
    result = subprocess.run(
        [sys.executable, "-m", "copyright_page.cli", "list-templates"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "default" in result.stdout


def test_cli_generate_markdown_to_stdout():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "copyright_page.cli",
            "generate",
            "--year",
            "2026",
            "--rights-holder",
            "Asdale Dynamics, LLC",
            "--isbn",
            "978-0-578-00000-0",
            "--edition",
            "First Edition",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "2026" in result.stdout
    assert "Asdale Dynamics, LLC" in result.stdout
    assert "978-0-578-00000-0" in result.stdout
    assert "First Edition" in result.stdout


def test_cli_generate_pdf_to_file(tmp_path):
    out = tmp_path / "copyright.pdf"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "copyright_page.cli",
            "generate",
            "--year",
            "2026",
            "--rights-holder",
            "Asdale Dynamics, LLC",
            "--isbn",
            "978-0-578-00000-0",
            "--edition",
            "First Edition",
            "--format",
            "pdf",
            "--output",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert out.is_file()
    assert out.read_bytes().startswith(b"%PDF")
