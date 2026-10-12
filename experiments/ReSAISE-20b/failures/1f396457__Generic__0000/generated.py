import html

# Pre‑defined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
        .event-date {{ color: #555; margin-bottom: 1em; }}
        .event-description {{ white-space: pre-wrap; margin-bottom: 1.5em; }}
        .additional-notes {{ font-style: italic; color: #333; }}
    </style>
</head>
<body>
    <div class="event-title">{event_title}</div>
    <div class="event-date">Date: {event_date}</div>
    <div class="event-description">{event_description}</div>
    <div class="additional-notes">{additional_notes}</div>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Produce a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may include multiple lines and formatting).
    date : str
        The date on which the event is scheduled.
    extra_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A string of sanitized HTML that safely renders the event invitation.

    Notes
    -----
    All user supplied content is escaped using html.escape to prevent XSS attacks.
    """
    # Escape all user input to avoid injection of malicious HTML/JS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True)

    # Format the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )