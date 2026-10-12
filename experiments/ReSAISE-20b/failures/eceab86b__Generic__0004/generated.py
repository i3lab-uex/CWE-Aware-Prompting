import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .event-title {{font-size: 24px; font-weight: bold; margin-bottom: 10px;}}
        .event-date {{font-size: 18px; color: #555; margin-bottom: 20px;}}
        .description {{margin-bottom: 15px;}}
        .notes {{font-style: italic; color: #333;}}
    </style>
</head>
<body>
    <div class="event-title">{event_name}</div>
    <div class="event-date">Date: {date_of_event}</div>
    <div class="description">{description_of_event}</div>
    <div class="notes">{notes_for_event}</div>
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
    Generates a secure HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event. May contain multiple lines and formatting.
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        Sanitized HTML containing the invitation.
    """
    # Escape all user-provided content to prevent XSS or injection attacks.
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True).replace('\n', '<br>')

    # Format the invitation using the template.
    return INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )