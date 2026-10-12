#!/usr/bin/env python3
"""
Generate a secure HTML invitation.

This module provides the `generate_event_html` function which takes raw user
supplied strings (title, description, date and extra notes) and produces a
sanitized HTML string using a predefined template.  All user data is escaped
to prevent XSS or other injection attacks, addressing the concerns of
CWE‑707 (Improper Neutralization of Input).

Author: ChatGPT
"""

from __future__ import annotations

import html
from typing import Final


# Pre‑defined HTML template with placeholders for the event data.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .invitation {{max-width: 600px; margin: auto; padding: 20px;
                       border: 1px solid #ddd; border-radius: 5px;}}
        h1 {{color: #2c3e50;}}
        .date {{font-weight: bold; color: #2980b9;}}
        .notes {{margin-top: 15px; font-style: italic; color: #7f8c8d;}}
    </style>
</head>
<body>
<div class="invitation">
    <h1>{event_title}</h1>
    <p class="date">{event_date}</p>
    <div>{event_description}</div>
    {additional_notes}
</div>
</body>
</html>
"""


def _escape_and_format(text: str) -> str:
    """
    Escape HTML special characters in *text* and replace newlines with <br> tags.
    This ensures that multiline user input is rendered correctly while remaining
    safe from injection attacks.

    Args:
        text: The raw user input string.

    Returns:
        A safe, HTML‑escaped string with line breaks preserved.
    """
    escaped = html.escape(text or "")
    return escaped.replace("\n", "<br>")


def generate_event_html(
    title: str,
    description: str,
    date: str,
    extra_notes: str | None = None,
) -> str:
    """
    Produce a sanitized HTML invitation string.

    All inputs are escaped to prevent XSS.  The function uses a simple
    string template and does not rely on external templating engines,
    keeping the dependency surface minimal.

    Args:
        title: The name or heading of the event.
        description: A detailed description (may contain multiple lines).
        date: The scheduled date of the event.
        extra_notes: Optional additional information or instructions.

    Returns:
        A fully formed, safe HTML string containing the invitation.
    """
    # Escape all user supplied fields
    safe_title = _escape_and_format(title)
    safe_description = _escape_and_format(description)
    safe_date = _escape_and_format(date)

    # Handle optional extra notes; if none, omit the section entirely
    if extra_notes:
        safe_notes = _escape_and_format(extra_notes)
        notes_html = f'<div class="notes">{safe_notes}</div>'
    else:
        notes_html = ""

    # Render the template with sanitized data
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=notes_html,
    )