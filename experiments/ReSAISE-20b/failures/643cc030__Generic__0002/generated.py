import html

# Pre‑defined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color:#333; }}
        .description, .notes {{ margin-top: 1rem; white-space: pre-wrap; }}
        .date {{ font-weight: bold; margin-top: 1rem; }}
    </style>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    {notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Produce a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The title or heading of the event.
    e_description : str
        A detailed description of the event. May contain line breaks or formatting.
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any additional notes or instructions from the user.

    Returns
    -------
    str
        A fully sanitized HTML string ready for safe rendering.
    """
    # Escape all user supplied content to avoid XSS attacks
    esc_title = html.escape(e_title, quote=True)
    esc_description = html.escape(e_description, quote=False)  # allow line breaks
    esc_date = html.escape(e_date, quote=True)
    esc_notes = html.escape(e_notes, quote=False)

    # Render the notes section only if notes are provided
    notes_section = f'<div class="notes"><strong>Notes:</strong><br>{esc_notes}</div>' if esc_notes.strip() else ''

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=esc_title,
        event_date=esc_date,
        event_description=esc_description,
        notes_section=notes_section
    )

    return invitation_html