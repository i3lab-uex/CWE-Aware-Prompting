import html

# Predefined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; }}
  .event-header {{ background-color:#f2f2f2; padding:10px; }}
  .event-body {{ margin-top:15px; }}
  .event-footer {{ margin-top:20px; font-size:0.9em; color:#555; }}
</style>
</head>
<body>
  <div class="event-header">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
  </div>
  <div class="event-body">
    {event_description}
  </div>
  <div class="event-footer">
    {additional_notes}
  </div>
</body>
</html>
"""

def generate_event_html(title: str, description: str,
                        date: str, extra_notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        A detailed description (may contain newlines).
    date : str
        The scheduled date of the event.
    extra_notes : str
        Any additional information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for rendering.
    """
    # Escape all user-provided content to neutralize potential XSS attacks.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace('\n', '<br>')

    # Construct the final HTML safely.
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )