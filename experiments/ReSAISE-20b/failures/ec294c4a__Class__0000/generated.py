import html

# Pre‑defined HTML template with placeholders for the invitation components.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family:Arial,Helvetica,sans-serif; margin:2em;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div style="margin-top:1em;">
        {event_description}
    </div>
    <hr style="margin:2em 0;">
    <p><em>{additional_notes}</em></p>
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
    Build a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        An extensive description of the event (may include newlines).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user supplied data to neutralize any HTML/JS injection attempts
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace('\n', '<br>')
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace('\n', '<br>')

    # Render the invitation using the sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html.strip()