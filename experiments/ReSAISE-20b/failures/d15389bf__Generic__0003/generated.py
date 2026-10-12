import html
from typing import Final

# Predefined HTML template with placeholders for safe substitution.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
    body {{font-family: Arial, sans-serif; margin: 20px;}}
    .invitation {{border: 1px solid #ccc; padding: 20px; border-radius: 5px;}}
    .event-title {{font-size: 1.8em; margin-bottom: 10px;}}
    .event-date {{color: #555; font-size: 1.2em; margin-bottom: 15px;}}
    .event-description {{margin-bottom: 20px; white-space: pre-wrap;}}
    .event-notes {{font-style: italic; color: #333;}}
</style>
</head>
<body>
<div class="invitation">
    <div class="event-title">{title}</div>
    <div class="event-date">Date: {date}</div>
    <div class="event-description">{description}</div>
    <div class="event-notes">{notes}</div>
</div>
</body>
</html>
"""

def generate_event_invite(
    title: str,
    description: str,
    date: str,
    notes: str
) -> str:
    """
    Generate a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or title of the event.
    description : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date : str
        The scheduled date for the event.
    notes : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML ready for safe display.
    """
    # Sanitize all user-provided input to prevent XSS or injection attacks
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True)

    # Render the invitation using the predefined template
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )