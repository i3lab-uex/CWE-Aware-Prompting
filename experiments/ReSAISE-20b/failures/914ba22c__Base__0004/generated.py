import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        .header {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .date {{ color: #555; margin-bottom: 20px; }}
        .description {{ margin-bottom: 20px; }}
        .notes {{ font-style: italic; color: #333; }}
    </style>
</head>
<body>
    <div class="header">{event_title}</div>
    <div class="date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    <div class="notes">{additional_notes}</div>
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
        A sanitized HTML string ready for safe display.
    """
    # Escape all user-provided content to prevent XSS (CWE-79).
    safe_title = html.escape(title, quote=True)
    # Preserve line breaks in description by converting them to <br> tags after escaping.
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )