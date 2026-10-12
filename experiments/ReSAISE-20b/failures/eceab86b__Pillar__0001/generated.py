import html
from typing import Optional

# Predefined HTML template.  The placeholders are named exactly as the function arguments.
INVITATION_FORMAT: str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .container {{max-width: 600px; margin: auto; padding: 20px; border:1px solid #ccc;}}
        h1 {{color:#2c3e50;}}
        .date, .notes {{font-weight: bold; margin-top: 10px;}}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_name}</h1>
    <p>{description_of_event}</p>
    <div class="date">Date: {date_of_event}</div>
    <div class="notes">{notes_for_event}</div>
</div>
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: Optional[str] = None
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        Title of the event.
    description_of_event : str
        Detailed description; may contain newlines or formatting.
    date_of_event : str
        Scheduled date string.
    notes_for_event : Optional[str]
        Additional user‑supplied notes.  Defaults to an empty string.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.

    Raises
    ------
    ValueError
        If any required argument is empty or not a string.
    """
    # Basic validation to guard against empty inputs
    for name, value in {
        "event_name": event_name,
        "description_of_event": description_of_event,
        "date_of_event": date_of_event
    }.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Argument '{name}' must be a non‑empty string")

    # Default notes to empty if None
    if notes_for_event is None:
        notes_for_event = ""

    # Escape all user inputs to prevent XSS and other injection attacks.
    escaped = {
        "event_name": html.escape(event_name, quote=True),
        "description_of_event": html.escape(description_of_event, quote=True).replace("\n", "<br>"),
        "date_of_event": html.escape(date_of_event, quote=True),
        "notes_for_event": html.escape(notes_for_event, quote=True).replace("\n", "<br>")
    }

    # Format the invitation using the predefined template.
    return INVITATION_FORMAT.format(**escaped)