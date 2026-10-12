import html

# Predefined HTML template with placeholders for the invitation data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .container {{max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd;}}
        h1 {{color: #2c3e50;}}
        .details, .extra {{margin-top: 15px;}}
    </style>
</head>
<body>
<div class="container">
    <h1>{title_of_event}</h1>
    <div class="details">{event_details}</div>
    <p><strong>Date:</strong> {scheduled_date}</p>
    <div class="extra">{extra_info}</div>
</div>
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
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Escape all user-supplied content to prevent XSS or HTML injection.
    safe_title = html.escape(title_of_event, quote=True)
    safe_details = html.escape(event_details, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_extra = html.escape(extra_info, quote=True).replace('\n', '<br>')

    # Format the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )
    return invitation_html