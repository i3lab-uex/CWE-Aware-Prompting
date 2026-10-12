import html

# Pre‑defined HTML template with placeholders for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; }}
  .event-title {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
  .event-date {{ color: #555; margin-bottom: 20px; }}
  .event-description {{ white-space: pre-wrap; margin-bottom: 20px; }}
  .additional-notes {{ font-style: italic; color: #333; }}
</style>
</head>
<body>
<div class="event-title">{event_title}</div>
<div class="event-date">Date: {event_date}</div>
<div class="event-description">{event_description}</div>
{additional_notes_section}
</body>
</html>
"""

def create_event_invitation(
    e_title: str,
    e_description: str,
    e_date: str,
    e_notes: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        An extensive description of the event (may include multiple lines and formatting).
    e_date : str
        The date on which the event is scheduled.
    e_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A fully escaped HTML string suitable for safe rendering.
    """
    # Escape all user‑supplied content to neutralize any HTML/JS injection attempts.
    escaped_title = html.escape(e_title, quote=True)
    escaped_description = html.escape(e_description, quote=True)
    escaped_date = html.escape(e_date, quote=True)
    escaped_notes = html.escape(e_notes, quote=True)

    # Build the notes section only if notes are provided.
    additional_notes_section = (
        f'<div class="additional-notes">Additional Notes: {escaped_notes}</div>'
        if escaped_notes.strip()
        else ''
    )

    # Format the invitation with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_date=escaped_date,
        event_description=escaped_description,
        additional_notes_section=additional_notes_section
    )

    return invitation_html