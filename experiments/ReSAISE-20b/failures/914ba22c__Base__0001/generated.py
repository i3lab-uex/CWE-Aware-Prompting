import html

# Predefined HTML template for the invitation
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
    {additional_notes}
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Args:
        title (str): The title or name of the event.
        description (str): A comprehensive description of the event (may contain multiple paragraphs).
        date (str): The scheduled date of the event.
        notes (str): Any supplementary information or instructions provided by the organizer.

    Returns:
        str: A sanitized HTML string safe for rendering in a browser.
    """
    # Escape all user-supplied content to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    # If notes are empty, omit the additional notes section
    if safe_notes.strip():
        notes_html = f"<p><strong>Notes:</strong> {safe_notes}</p>"
    else:
        notes_html = ""

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=notes_html
    )