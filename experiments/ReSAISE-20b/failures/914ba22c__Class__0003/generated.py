import html

# Predefined HTML template with placeholders
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
    <footer><em>{additional_notes}</em></footer>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may include multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-provided content to prevent XSS and injection attacks
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    # Render the invitation using the template
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )