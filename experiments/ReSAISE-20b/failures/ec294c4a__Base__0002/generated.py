import html

# Pre‑defined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
</head>
<body>
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    <footer><small>{additional_notes}</small></footer>
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
    Build a secure HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A comprehensive description of the event (may include newlines and basic formatting).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string that safely renders the event invitation.
    """
    # Escape all user‑supplied content to neutralise potential XSS payloads.
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Inject the escaped values into the template.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )

    return invitation_html