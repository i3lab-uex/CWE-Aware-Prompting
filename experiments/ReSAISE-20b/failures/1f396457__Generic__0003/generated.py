# -*- coding: utf-8 -*-
"""
Secure event invitation HTML generator.
"""

import html
from typing import Final

# Pre‑defined template with placeholders.  The placeholder names must match the
# arguments of ``generate_event_html``.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
        .event-title {{ font-size: 24px; margin-bottom: 10px; }}
        .event-date {{ color: #555; font-weight: bold; margin-bottom: 20px; }}
        .event-description {{ white-space: pre-wrap; }}
        .additional-notes {{ margin-top: 20px; font-style: italic; color: #333; }}
    </style>
</head>
<body>
<div class="invitation">
    <div class="event-title">{event_title}</div>
    <div class="event-date">Date: {event_date}</div>
    <div class="event-description">{event_description}</div>
    {additional_notes_block}
</div>
</body>
</html>
"""

def _escape(text: str) -> str:
    """
    Escape a string for safe inclusion in HTML.

    Args:
        text: The raw user supplied text.

    Returns:
        A string safe for rendering in HTML.
    """
    return html.escape(text, quote=True)

def generate_event_html(
    title: str,
    description: str,
    date: str,
    extra_notes: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may include newlines).
    date : str
        The scheduled date of the event.
    extra_notes : str
        Any additional information or instructions supplied by the user.

    Returns
    -------
    str
        A fully rendered, safe HTML string ready for display or email.

    Raises
    ------
    ValueError
        If any required argument is empty or None.
    """
    # Basic validation
    for name, value in (("title", title), ("description", description),
                        ("date", date), ("extra_notes", extra_notes)):
        if value is None:
            raise ValueError(f"Argument '{name}' cannot be None")

    # Escape user content
    safe_title = _escape(title)
    safe_description = _escape(description).replace("\n", "<br>")
    safe_date = _escape(date)
    safe_notes = _escape(extra_notes).replace("\n", "<br>")

    # Build optional notes block
    additional_notes_block = ""
    if safe_notes.strip():
        additional_notes_block = f'<div class="additional-notes">{safe_notes}</div>'

    # Render the template
    html_output = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_block=additional_notes_block
    )
    return html_output.strip()