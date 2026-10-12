import html

# Predefined HTML template with placeholders for the event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
        h1 {{ color: #333; }}
        .date {{ font-weight: bold; margin-bottom: 15px; }}
        .notes {{ margin-top: 20px; font-style: italic; color: #555; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_title}</h1>
    <div class="date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    <div class="notes">Additional Notes: {additional_notes}</div>
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may contain multiple paragraphs).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        A sanitized HTML string ready for secure display.
    """
    # Sanitize all user-provided content to prevent XSS attacks.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace('\n', '<br>')

    # Populate the template with sanitized values.
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )