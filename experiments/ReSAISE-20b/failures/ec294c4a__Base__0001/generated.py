import html

# Pre‑defined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    <footer>{additional_notes}</footer>
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
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description of the event (may contain line breaks).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions supplied by the user.

    Returns
    -------
    str
        A string containing a fully sanitized HTML invitation.
    """
    # Escape all user supplied data to neutralize any potential XSS payloads.
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Format the invitation using the safe values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return invitation_html