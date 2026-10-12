import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px;}}
        .event-title {{font-size: 24px; font-weight: bold; margin-bottom: 10px;}}
        .event-date {{color: #555; margin-bottom: 20px;}}
        .event-description, .additional-notes {{margin-bottom: 15px; white-space: pre-wrap;}}
    </style>
</head>
<body>
    <div class="event-title">{event_title}</div>
    <div class="event-date">Date: {event_date}</div>
    <div class="event-description">{event_description}</div>
    <div class="additional-notes"><strong>Additional Notes:</strong><br>{additional_notes}</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description (may include newlines).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape user-provided content to prevent XSS
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=True)
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=True)

    # Format the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )

    return invitation_html