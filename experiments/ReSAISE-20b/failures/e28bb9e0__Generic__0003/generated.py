import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
  .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
  .event-title {{ font-size: 24px; margin-bottom: 10px; }}
  .event-date {{ color: #555; margin-bottom: 20px; }}
  .event-description {{ white-space: pre-wrap; }}
  .additional-notes {{ margin-top: 20px; font-style: italic; color: #333; }}
</style>
</head>
<body>
<div class="invitation">
  <div class="event-title">{event_title}</div>
  <div class="event-date">{event_date}</div>
  <div class="event-description">{event_description}</div>
  {additional_notes_block}
</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may include multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        A string containing sanitized HTML for secure display of the event invitation.
    """
    # Escape all user-provided content to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Render additional notes block only if notes are provided
    additional_notes_block = (
        f'<div class="additional-notes">{safe_notes}</div>'
        if notes.strip()
        else ""
    )

    # Format the final HTML using the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_block=additional_notes_block,
    )

    return invitation_html