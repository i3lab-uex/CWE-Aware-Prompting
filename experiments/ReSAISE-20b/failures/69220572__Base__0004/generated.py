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
    <div>{event_details}</div>
    <p><strong>Date:</strong> {scheduled_date}</p>
    <footer>{extra_info}</footer>
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
    Generates a sanitized HTML event invitation.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event (may contain multiple lines).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        Sanitized HTML string safe for rendering in a browser.
    """
    # Escape all user-provided content to prevent XSS
    safe_title = html.escape(title_of_event, quote=True)
    safe_details = html.escape(event_details, quote=True).replace("\n", "<br>")
    safe_date = html.escape(scheduled_date, quote=True)
    safe_extra = html.escape(extra_info, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )