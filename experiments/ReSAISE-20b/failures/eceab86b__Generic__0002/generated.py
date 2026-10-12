import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px;}}
        .event-title {{font-size: 24px; font-weight: bold; margin-bottom: 10px;}}
        .event-date {{font-size: 18px; color: #555; margin-bottom: 20px;}}
        .event-description {{margin-bottom: 20px; white-space: pre-wrap;}}
        .event-notes {{font-style: italic; color: #333;}}
    </style>
</head>
<body>
    <div class="event-title">{event_name}</div>
    <div class="event-date">Date: {date_of_event}</div>
    <div class="event-description">{description_of_event}</div>
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
        The name or title of the event.
    description_of_event : str
        A comprehensive description (may contain line breaks).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering.
    """
    # Escape all user-provided content to prevent XSS.
    escaped_name = html.escape(event_name, quote=True)
    escaped_desc = html.escape(description_of_event, quote=True)
    escaped_date = html.escape(date_of_event, quote=True)

    # If notes are provided, escape and wrap them in a div.
    if notes_for_event:
        escaped_notes = html.escape(notes_for_event, quote=True)
        notes_block = f'<div class="event-notes">Notes: {escaped_notes}</div>'
    else:
        notes_block = ''

    # Populate the template.
    invitation_html = INVITATION_FORMAT.format(
        event_name=escaped_name,
        description_of_event=escaped_desc,
        date_of_event=escaped_date,
        notes_block=notes_block
    )

    return invitation_html