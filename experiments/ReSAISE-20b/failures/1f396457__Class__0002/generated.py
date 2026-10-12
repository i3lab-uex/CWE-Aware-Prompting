import html

# Pre‑defined template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
  .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
  .event-date {{ color: #555; margin-bottom: 1em; }}
  .event-description {{ margin-bottom: 1em; white-space: pre-wrap; }}
  .extra-notes {{ font-style: italic; color: #333; }}
</style>
</head>
<body>
  <div class="event-title">{event_title}</div>
  <div class="event-date">Date: {event_date}</div>
  <div class="event-description">{event_description}</div>
  <div class="extra-notes">{additional_notes}</div>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may include multiple lines).
    date : str
        The scheduled date of the event.
    extra_notes : str
        Any additional information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in browsers.
    """
    # Escape all user supplied values to prevent XSS and injection attacks
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True)

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )