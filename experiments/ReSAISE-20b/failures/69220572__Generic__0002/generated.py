import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
        .event-details {{ white-space: pre-wrap; margin-bottom: 1em; }}
        .event-date, .extra-info {{ color: #555; margin-bottom: 0.5em; }}
    </style>
</head>
<body>
    <div class="event-title">{title_of_event}</div>
    <div class="event-details">{event_details}</div>
    <div class="event-date"><strong>Date:</strong> {scheduled_date}</div>
    <div class="extra-info">{extra_info}</div>
</body>
</html>
"""

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a sanitized HTML event invitation.

    Parameters:
        title_of_event (str): The name or title of the event.
        event_details (str): A comprehensive description of the event.
        scheduled_date (str): The scheduled date for the event.
        extra_info (str): Extra information or instructions.

    Returns:
        str: A string containing sanitized HTML suitable for safe display.
    """
    # Escape all user-provided content to prevent XSS attacks.
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_details = html.escape(event_details, quote=True)
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_extra = html.escape(extra_info, quote=True)

    # Render the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=escaped_title,
        event_details=escaped_details,
        scheduled_date=escaped_date,
        extra_info=escaped_extra
    )
    return invitation_html