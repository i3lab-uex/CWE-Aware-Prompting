import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event}</title>
</head>
<body style="font-family:Arial,Helvetica,sans-serif; margin:20px;">
    <h1>{title_of_event}</h1>
    <p><strong>Date:</strong> {scheduled_date}</p>
    <hr>
    <div>{event_details}</div>
    <hr>
    {extra_info}
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
        A comprehensive description (may contain multiple lines).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions.

    Returns
    -------
    str
        A string containing the sanitized HTML invitation.
    """
    # Escape all user-supplied content to neutralize special characters.
    safe_title = html.escape(title_of_event, quote=True)
    safe_date = html.escape(scheduled_date, quote=True)

    # Escape details and preserve line breaks by converting \n to <br>.
    safe_details = html.escape(event_details, quote=True).replace('\n', '<br>')

    # Escape extra info; if it contains HTML we want to treat it as plain text.
    safe_extra = html.escape(extra_info, quote=True).replace('\n', '<br>')

    # Format the invitation using the safe values.
    return INVITATION_FORMAT.format(
        title_of_event=safe_title,
        scheduled_date=safe_date,
        event_details=safe_details,
        extra_info=safe_extra
    )