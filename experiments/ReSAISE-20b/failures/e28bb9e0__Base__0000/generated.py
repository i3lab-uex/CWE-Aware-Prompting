import html

# Predefined HTML template with placeholders for safe substitution.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{font-family: Arial, sans-serif; margin: 20px;}}
    .invitation {{border:1px solid #ccc; padding:15px; border-radius:5px;}}
    .header {{font-size:1.5em; margin-bottom:10px;}}
    .date {{color:#555; font-style:italic; margin-bottom:15px;}}
</style>
</head>
<body>
<div class="invitation">
    <div class="header">{event_title}</div>
    <div class="date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    <div class="notes">{additional_notes}</div>
</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description of the event (may contain multiple paragraphs).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-provided content to neutralize potential XSS payloads
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    # Format the invitation using the predefined template
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )