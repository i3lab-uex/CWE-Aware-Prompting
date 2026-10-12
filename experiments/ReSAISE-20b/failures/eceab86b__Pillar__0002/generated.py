import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_name} Invitation</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
  .event-header {{ font-size: 24px; margin-bottom: 10px; }}
  .event-date {{ color: #555; margin-bottom: 20px; }}
  .description {{ white-space: pre-wrap; }}
  .notes {{ margin-top: 20px; font-style: italic; color: #333; }}
</style>
</head>
<body>
  <div class="event-header">{event_name}</div>
  <div class="event-date">Date: {date_of_event}</div>
  <div class="description">{description_of_event}</div>
  {notes_block}
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The title of the event.
    description_of_event : str
        A detailed, possibly multiline, description of the event.
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Additional instructions or notes.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in browsers.
    """
    # Escape all user supplied content to avoid injection
    esc_event_name = html.escape(event_name, quote=True)
    esc_description = html.escape(description_of_event, quote=True)
    esc_date = html.escape(date_of_event, quote=True)

    # Handle notes: only include if non-empty
    if notes_for_event.strip():
        esc_notes = html.escape(notes_for_event, quote=True)
        notes_block = f'<div class="notes">{esc_notes}</div>'
    else:
        notes_block = ''

    invitation_html = INVITATION_FORMAT.format(
        event_name=esc_event_name,
        description_of_event=esc_description,
        date_of_event=esc_date,
        notes_block=notes_block
    )
    return invitation_html