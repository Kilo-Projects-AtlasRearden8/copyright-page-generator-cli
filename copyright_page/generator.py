"""Rendering copyright page Markdown from templates and context values."""

from __future__ import annotations

from typing import Any, Dict

from .templates import DEFAULT_PLACEHOLDERS, TemplateError, load_template


class RenderError(ValueError):
    """Raised when a copyright page cannot be rendered."""


def validate_context(context: Dict[str, Any]) -> None:
    """Ensure every required placeholder has a non-empty value."""
    missing = [key for key in DEFAULT_PLACEHOLDERS if not str(context.get(key, "")).strip()]
    if missing:
        raise RenderError("Missing required values: " + ", ".join(missing))


def render_template(name: str, context: Dict[str, Any], templates_dir: str | None = None) -> str:
    """Render a named template with the given context values.

    Placeholders are {year}, {rights_holder}, {isbn}, and {edition}.
    """
    validate_context(context)
    template = load_template(name, templates_dir)
    try:
        return template["markdown"].format(**context)
    except KeyError as exc:
        raise RenderError(f"Template references unknown placeholder: {exc}") from exc


def render(context: Dict[str, Any], template_name: str = "default", templates_dir: str | None = None) -> str:
    """Convenience wrapper around render_template."""
    return render_template(template_name, context, templates_dir)
