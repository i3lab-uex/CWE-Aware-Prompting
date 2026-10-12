#!/usr/bin/env python3
"""
generate_event_invite.py

A utility to produce a secure, sanitized HTML invitation for an event.
The function ensures that all user supplied content is escaped to prevent
XSS and other injection attacks (CWE-707: Improper Neutralization of Input).
"""

import html
from typing import Final

# Predefined HTML template with placeholders.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .date, .notes {{ margin-top: 10px; font-weight: bold; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_title}</h1>
    <div class="date">Date: {event_date}</div>
    <hr/>
    <div class="description">{event_description}</div>
    {notes_block}
</div>
</body>
</html>
"""

def _escape_and_convert_paragraphs(text: str) -> str:
    """
    Escapes HTML special characters and preserves paragraph breaks.
    Paragraphs are detected by double newlines.
    """
    escaped = html.escape(text)
    # Replace paragraph separators with <p> tags
    paragraphs = [f"<p>{para.strip()}</p>" for para in escaped.split("\n\n") if para.strip()]
    return "\n".join(paragraphs)

def generate_event_invite(
    title: str,
    description: str,
    date: str,
    notes: str
) -> str:
    """
    Generates a sanitized HTML invitation string.

    Parameters
    ----------
    title : str
        The event's title.
    description : str
        Detailed, possibly multi‑paragraph description.
    date : str
        The scheduled date of the event.
    notes : str
        Additional instructions or supplementary information.

    Returns
    -------
    str
        A fully sanitized HTML invitation ready for safe rendering.
    """
    # Sanitize all inputs
    safe_title = html.escape(title)
    safe_date = html.escape(date)

    # Convert description paragraphs
    safe_description = _escape_and_convert_paragraphs(description)

    # Notes are optional; if provided, escape and wrap in a div
    if notes.strip():
        safe_notes = html.escape(notes).replace("\n", "<br/>")
        notes_block = f'<div class="notes">Additional Notes:<br/>{safe_notes}</div>'
    else:
        notes_block = ""

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        notes_block=notes_block
    )
    return invitation_html

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     html_invite = generate_event_invite(
#         title="Annual Gala",
#         description="Join us for an evening of celebration.\n\nWe will have live music and a dinner.",
#         date="2026-08-15",
#         notes="Please RSVP by 2026-07-31."
#     )
#     print(html_invite)