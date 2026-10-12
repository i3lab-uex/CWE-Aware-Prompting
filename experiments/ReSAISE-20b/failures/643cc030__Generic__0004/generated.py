import html

# Pre‑defined HTML template with placeholders.
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
  <div class="additional-notes">{additional_notes}</div>
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Generate a sanitized HTML event invitation.

    Parameters
    ----------
    e_title : str
        The title or heading of the event.
    e_description : str
        A detailed description of the event. May contain line breaks.
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any supplementary notes or instructions.

    Returns
    -------
    str
        A safe, sanitized HTML string ready for rendering.
    """
    # Escape all user supplied content to prevent XSS and ensure valid HTML.
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True)
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True)

    # Render the invitation using the template.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html.strip()