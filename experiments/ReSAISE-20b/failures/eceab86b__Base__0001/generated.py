import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .event-header {{ background:#f4f4f4; padding:10px; margin-bottom:15px; }}
        .event-date {{ font-weight:bold; color:#333; }}
        .notes {{ margin-top:20px; background:#e8f4ff; padding:10px; }}
    </style>
</head>
<body>
    <div class="event-header">
        <h1>{event_name}</h1>
        <p class="event-date">Date: {date_of_event}</p>
    </div>
    <div class="event-description">
        <pre>{description_of_event}</pre>
    </div>
    {notes_section}
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain multiple lines).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML suitable for safe rendering in a browser.

    Notes
    -----
    All user-supplied content is escaped using html.escape to mitigate XSS (CWE-79).
    The function does not perform additional sanitization beyond escaping.
    """
    # Escape all user-provided content
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True)
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True)

    # Prepare the notes section only if notes are provided
    if safe_notes.strip():
        notes_section = f'<div class="notes"><h2>Additional Notes</h2><p>{safe_notes}</p></div>'
    else:
        notes_section = ''

    # Render the final HTML using the template
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_section=notes_section
    )
    return invitation_html