"""Loading and validation of local JSON copyright page templates."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

DEFAULT_PLACEHOLDERS = ("year", "rights_holder", "isbn", "edition")


class TemplateError(ValueError):
    """Raised when a template is missing, malformed, or unusable."""


def _default_templates_dir() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def load_template(name: str, templates_dir: str | None = None) -> Dict[str, Any]:
    """Load a single template by name from the local JSON templates directory."""
    templates_dir = templates_dir or _default_templates_dir()
    path = os.path.join(templates_dir, f"{name}.json")
    if not os.path.isfile(path):
        raise TemplateError(f"Template not found: {name} (looked in {templates_dir})")
    with open(path, "r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise TemplateError(f"Template {name} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise TemplateError(f"Template {name} must be a JSON object")
    if "markdown" not in data or not isinstance(data["markdown"], str):
        raise TemplateError(f"Template {name} must include a 'markdown' string")
    data.setdefault("name", name)
    data.setdefault("description", "")
    return data


def list_templates(templates_dir: str | None = None) -> List[Dict[str, str]]:
    """Return metadata for every template available in the templates directory."""
    templates_dir = templates_dir or _default_templates_dir()
    results: List[Dict[str, str]] = []
    if not os.path.isdir(templates_dir):
        return results
    for filename in sorted(os.listdir(templates_dir)):
        if not filename.endswith(".json"):
            continue
        try:
            data = load_template(filename[:-5], templates_dir)
        except TemplateError:
            continue
        results.append(
            {"name": data.get("name", filename[:-5]), "description": data.get("description", "")}
        )
    return results
