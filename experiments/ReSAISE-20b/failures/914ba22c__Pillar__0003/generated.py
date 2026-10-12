import html
from typing import Final

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title} - Invitation</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    .header {{ background-color: #f2f2f2; padding: 10px; }}
    .content {{ margin-top: 15px; }}
    .footer {{ margin-top: 20px; font-size: 0.9em; color: #555; }}
</style>
</head>
<body>
<div class="header">
    <h1>{event_title}</h1>
</div>
<div class="content">
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
</div>
<div class="footer">
    {additional_notes}
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a secure HTML representation of an event invitation.

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
        A sanitized HTML string ready for secure display.
    """
    # Escape all user-provided content to prevent XSS or injection
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    # Format the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )