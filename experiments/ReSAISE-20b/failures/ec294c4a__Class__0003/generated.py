import html

# Pre‑defined HTML template with placeholders
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
        .event-description, .additional-notes {{margin-bottom: 15px;}}
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

def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str
) -> str:
    """
    Construct a sanitized HTML invitation for an event.

    Parameters:
        title_of_event (str): The name or heading of the event.
        details_of_event (str): An extensive description of the event
            (may include multiple lines and formatting).
        when_event_is (str): The date on which the event is scheduled.
        extra_event_info (str): Any extra information or instructions
            supplied by the user.

    Returns:
        str: A sanitized HTML string that safely renders the invitation.
    """
    # Escape all user supplied content to prevent XSS or injection
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_description = html.escape(details_of_event, quote=True).replace('\n', '<br>')
    escaped_date = html.escape(when_event_is, quote=True)
    escaped_notes = html.escape(extra_event_info, quote=True).replace('\n', '<br>')

    # Format the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_date=escaped_date,
        event_description=escaped_description,
        additional_notes=escaped_notes
    )
    return invitation_html