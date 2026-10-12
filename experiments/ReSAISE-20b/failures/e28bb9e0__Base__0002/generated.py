import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    <hr/>
    <div><em>Additional Notes:</em> {additional_notes}</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML event invitation.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description of the event (may contain multiple paragraphs).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions from the organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for secure display.
    """
    # Escape all user-provided content to prevent XSS (CWE-79).
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )