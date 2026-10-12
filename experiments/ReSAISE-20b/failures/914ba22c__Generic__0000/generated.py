import html
from string import Template

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$event_title</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 20px;}
        .invite-header {font-size: 1.5em; font-weight: bold;}
        .invite-date   {color: #555;}
        .invite-desc   {margin-top: 15px;}
        .invite-notes  {margin-top: 20px; font-style: italic; color: #333;}
    </style>
</head>
<body>
    <div class="invite-header">$event_title</div>
    <div class="invite-date">Date: $event_date</div>
    <div class="invite-desc">$event_description</div>
    <div class="invite-notes">$additional_notes</div>
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
    # Sanitize each input to prevent XSS attacks
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    template = Template(INVITATION_FORMAT)
    return template.substitute(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )