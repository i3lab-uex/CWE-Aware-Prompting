import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event}</title>
</head>
<body>
    <h1>{title_of_event}</h1>
    <p><strong>Date:</strong> {scheduled_date}</p>
    <div>{event_details}</div>
    <footer><em>{extra_info}</em></footer>
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
    Generates a sanitized HTML representation of an event invitation.

    Args:
        title_of_event (str): The name or title of the event.
        event_details (str): A comprehensive description of the event. May contain
                             multiple lines and formatting.
        scheduled_date (str): The scheduled date for the event.
        extra_info (str): Extra information or instructions provided by the user.

    Returns:
        str: A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Escape all user-provided input to neutralize potential XSS content
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_details = html.escape(event_details, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_extra = html.escape(extra_info, quote=True).replace("\n", "<br>")

    # Format the invitation using the template
    return INVITATION_FORMAT.format(
        title_of_event=escaped_title,
        event_details=escaped_details,
        scheduled_date=escaped_date,
        extra_info=escaped_extra
    )