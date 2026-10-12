import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; }}
  .invitation {{ border: 1px solid #ccc; padding: 20px; border-radius: 5px; }}
  .title {{ font-size: 1.8em; margin-bottom: 10px; }}
  .date {{ color: #555; margin-bottom: 15px; }}
  .description, .notes {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<div class="invitation">
  <div class="title">{event_title}</div>
  <div class="date">Date: {event_date}</div>
  <div class="description">{event_description}</div>
  {additional_notes_section}
</div>
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The title of the event.
    e_description : str
        A detailed description, possibly multiline.
    e_date : str
        The date of the event.
    e_notes : str
        Optional extra information or instructions.

    Returns
    -------
    str
        A sanitized HTML string representing the invitation.
    """
    # Escape all user-supplied content to prevent injection attacks
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True)
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True)

    # Conditionally include the notes section only if notes are provided
    additional_notes_section = (
        f'<div class="notes"><strong>Additional Notes:</strong><br>{safe_notes}</div>'
        if safe_notes.strip()
        else ''
    )

    # Render the final HTML using the sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_section=additional_notes_section
    )

    return invitation_html