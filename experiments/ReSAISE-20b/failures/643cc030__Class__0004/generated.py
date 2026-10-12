import html

# Pre‑defined HTML template with placeholders for the event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #2c3e50; }}
        .date {{ font-weight: bold; margin-top: 1rem; }}
        .notes {{ margin-top: 2rem; color: #7f8c8d; }}
    </style>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="description">
        {event_description}
    </div>
    <p class="date">Date: {event_date}</p>
    {additional_notes}
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description of the event. May contain multiple lines.
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string containing the invitation content.
    """
    # Escape all user supplied data to prevent injection attacks (CWE‑74).
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=False).replace('\n', '<br>')
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=False).replace('\n', '<br>')

    # If notes are provided, wrap them in a dedicated section.
    notes_html = f'<div class="notes">{safe_notes}</div>' if e_notes.strip() else ''

    # Format the final HTML with the sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=notes_html
    )
    return invitation_html