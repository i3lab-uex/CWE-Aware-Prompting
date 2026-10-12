import html

# Pre‑defined HTML template with named placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} – Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
        .event-date {{ color: #555; margin-bottom: 1em; }}
        .description, .notes {{ white-space: pre-wrap; margin-bottom: 1em; }}
    </style>
</head>
<body>
    <div class="event-title">{event_title}</div>
    <div class="event-date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    {notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Return a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description of the event. May contain newlines and formatting.
    e_date : str
        The date on which the event is scheduled.
    e_notes : str
        Any additional information or instructions provided by the user.

    Returns
    -------
    str
        A fully escaped, well‑formed HTML string ready for safe rendering.

    Raises
    ------
    ValueError
        If any required argument is empty or consists only of whitespace.
    """
    # Basic validation: ensure mandatory fields are present
    for name, value in (("Title", e_title), ("Description", e_description),
                        ("Date", e_date)):
        if not value or not value.strip():
            raise ValueError(f"{name} cannot be empty.")

    # Escape all user‑supplied content to prevent XSS and other injection
    escaped_title = html.escape(e_title, quote=True)
    escaped_description = html.escape(e_description, quote=True)
    escaped_date = html.escape(e_date, quote=True)

    # Handle optional notes: only include the section if there is meaningful content
    if e_notes and e_notes.strip():
        escaped_notes = html.escape(e_notes, quote=True)
        notes_section = f'<div class="notes">Notes: {escaped_notes}</div>'
    else:
        notes_section = ''

    # Safely format the template with the escaped values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_date=escaped_date,
        event_description=escaped_description,
        notes_section=notes_section
    )

    return invitation_html