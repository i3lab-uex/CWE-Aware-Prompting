import html

# Pre‑defined HTML template with placeholders for the invitation data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    .event-title {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
    .event-date {{ color: #555; margin-bottom: 1rem; }}
    .event-description {{ white-space: pre-wrap; }}
    .additional-notes {{ margin-top: 1.5rem; font-style: italic; }}
</style>
</head>
<body>
    <h1 class="event-title">{event_title}</h1>
    <div class="event-date"><strong>Date:</strong> {event_date}</div>
    <div class="event-description">{event_description}</div>
    <div class="additional-notes">{additional_notes}</div>
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
        An extensive description of the event (may contain newlines).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions supplied by the user.

    Returns
    -------
    str
        A fully sanitized HTML string ready to be served.
    """
    # Escape all user‑supplied content to neutralise any HTML or script injection.
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True)
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True)

    # Populate the template safely.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return invitation_html.strip()