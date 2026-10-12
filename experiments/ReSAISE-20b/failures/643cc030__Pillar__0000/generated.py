#!/usr/bin/env python3
"""
Secure event invitation generator.

This module defines a single public function, `create_event_invitation`, which
produces an HTML representation of an event invitation. All user supplied data
is properly escaped to prevent cross‑site scripting and other injection attacks.
"""

import html

# --------------------------------------------------------------------------- #
# 1. Default invitation template
# --------------------------------------------------------------------------- #
INVITATION_FORMAT: str = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
    .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
    h1 {{ color: #333; }}
    .date {{ font-weight: bold; margin-bottom: 10px; }}
</style>
</head>
<body>
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="date">{event_date}</div>
    <p>{event_description}</p>
    {additional_notes}
</div>
</body>
</html>
"""

# --------------------------------------------------------------------------- #
# 2. Helper functions
# --------------------------------------------------------------------------- #
def _escape_and_format(text: str, allow_br: bool = False) -> str:
    """
    Escape HTML special characters in *text* and optionally convert newlines to <br> tags.
    """
    escaped = html.escape(text, quote=True)
    if allow_br:
        escaped = escaped.replace("\n", "<br>")
    return escaped

def _format_notes(notes: str) -> str:
    """
    Render the notes section. If *notes* is empty or only whitespace, return an empty string.
    """
    if not notes.strip():
        return ""
    # Wrap the notes in a paragraph for consistency
    escaped = _escape_and_format(notes, allow_br=True)
    return f"<p>{escaped}</p>"

# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #
def create_event_invitation(
    e_title: str,
    e_description: str,
    e_date: str,
    e_notes: str
) -> str:
    """
    Generate a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description of the event. May contain newlines and formatting.
    e_date : str
        The date on which the event is scheduled.
    e_notes : str
        Any additional information or instructions supplied by the user.

    Returns
    -------
    str
        A string containing sanitized HTML that renders the event invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checking (defensive programming)
    for name, value in {
        "e_title": e_title,
        "e_description": e_description,
        "e_date": e_date,
        "e_notes": e_notes
    }.items():
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")

    # Escape each component. Preserve line breaks in description and notes.
    title_escaped = _escape_and_format(e_title)
    desc_escaped = _escape_and_format(e_description, allow_br=True)
    date_escaped = _escape_and_format(e_date)
    notes_formatted = _format_notes(e_notes)

    # Use a dictionary for safe formatting; avoid format specifiers in user data.
    payload = {
        "event_title": title_escaped,
        "event_description": desc_escaped,
        "event_date": date_escaped,
        "additional_notes": notes_formatted
    }

    # Render the final HTML. Using format_map to prevent accidental specifier usage.
    invitation_html = INVITATION_FORMAT.format(**payload)
    return invitation_html

# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample = create_event_invitation(
        e_title="Annual Gala",
        e_description=(
            "Join us for an evening of celebration and networking.\n"
            "Dress code: Black tie."
        ),
        e_date="December 15, 2024",
        e_notes=(
            "Please RSVP by December 1.\n"
            "For assistance, contact <support@example.com>."
        )
    )
    print(sample)