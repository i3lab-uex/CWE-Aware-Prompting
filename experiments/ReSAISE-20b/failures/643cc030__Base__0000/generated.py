import html

# Predefined HTML template with placeholders for safe insertion.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #2c3e50; }}
        .description, .notes {{ margin-top: 1rem; white-space: pre-wrap; }}
        .date {{ color: #7f8c8d; margin-top: 0.5rem; }}
    </style>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="date"><strong>Date:</strong> {event_date}</div>
    <div class="description"><strong>Description:</strong><br>{event_description}</div>
    {additional_notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        An extensive description (may contain line breaks or formatting).
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A string containing safe, sanitized HTML ready for rendering.
    """
    # Escape all user-controllable input to prevent XSS
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True)
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True)

    # Render additional notes only if provided
    if safe_notes.strip():
        notes_html = f'<div class="notes"><strong>Additional Notes:</strong><br>{safe_notes}</div>'
    else:
        notes_html = ''

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=notes_html
    )

    return invitation_html