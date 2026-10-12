import html

# Pre‑defined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <hr/>
    <div>{event_description}</div>
    <hr/>
    {additional_notes}
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
    Build a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        An extensive description of the event (may include multiple lines and formatting).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A string of sanitized HTML that safely renders the event invitation.
    """
    # Escape all user supplied content to prevent XSS or injection attacks.
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=False).replace('\n', '<br/>')
    safe_date = html.escape(when_event_is, quote=True)
    if extra_event_info.strip():
        safe_notes = f"<p><em>{html.escape(extra_event_info, quote=False).replace('\n', '<br/>')}</em></p>"
    else:
        safe_notes = ""

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )