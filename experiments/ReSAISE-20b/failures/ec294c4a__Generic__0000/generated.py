import html

# Pre‑defined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .invitation {{ border: 1px solid #ccc; padding: 1rem; border-radius: 5px; }}
        .date {{ color: #555; margin-top: 0.5rem; }}
        .notes {{ font-size: 0.9rem; color: #333; margin-top: 1rem; }}
    </style>
</head>
<body>
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="date"><strong>Date:</strong> {event_date}</div>
    <p>{event_description}</p>
    <div class="notes">{additional_notes}</div>
</div>
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
        A sanitized HTML string ready to be served.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=False).replace('\n', '<br>')
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=False).replace('\n', '<br>')

    # Render the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )

    return invitation_html