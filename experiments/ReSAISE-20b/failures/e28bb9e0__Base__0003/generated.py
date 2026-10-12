# -*- coding: utf-8 -*-
"""
Secure event invitation generator.

This module defines a single public function `create_event_invitation` that
produces an HTML representation of an event invitation.  All user‑supplied
content is properly escaped to prevent Cross‑Site Scripting (XSS) attacks.
"""

from __future__ import annotations

import html
from typing import Final

# A minimal, safe HTML template with placeholders for the invitation fields.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .notes {{ margin-top: 20px; font-style: italic; color: #555; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="description">{event_description}</div>
    {additional_notes}
</div>
</body>
</html>
"""


def _sanitize(text: str) -> str:
    """
    Escape HTML special characters to prevent XSS.
    Newlines are converted to <br> tags for readability.
    """
    escaped = html.escape(text, quote=True)
    return escaped.replace("\n", "<br>")


def create_event_invitation(
    title: str,
    description: str,
    date: str,
    notes: str = "",
) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event. May contain multiple paragraphs.
    date : str
        The scheduled date of the event.
    notes : str, optional
        Supplementary information or instructions from the organizer.

    Returns
    -------
    str
        A sanitized HTML string ready for safe display in a web page.

    Notes
    -----
    All input strings are escaped to neutralize any embedded HTML or JavaScript.
    """
    # Sanitize all user inputs
    safe_title = _sanitize(title)
    safe_description = _sanitize(description)
    safe_date = _sanitize(date)
    safe_notes = _sanitize(notes)

    # Prepare the notes block only if notes are provided
    additional_notes_block = (
        f'<div class="notes">{safe_notes}</div>' if safe_notes else ""
    )

    # Populate the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=additional_notes_block,
    )

    return invitation_html