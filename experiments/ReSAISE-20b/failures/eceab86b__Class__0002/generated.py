import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
        .event-date {{ color: #555; margin-bottom: 1em; }}
        .description, .notes {{ white-space: pre-wrap; margin-bottom: 1em; }}
    </style>
</head>
<body>
    <div class="event-title">{event_name}</div>
    <div class="event-date">Date: {date_of_event}</div>
    <div class="description">{description_of_event}</div>
    <div class="notes"><strong>Notes:</strong> {notes_for_event}</div>
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
    Generates a sanitized HTML invitation for an event.

    Args:
        event_name: The title of the event.
        description_of_event: A detailed, possibly multiline description.
        date_of_event: The scheduled date for the event.
        notes_for_event: Additional instructions or information.

    Returns:
        A string containing safe, escaped HTML ready for display.
    """
    # Escape all user-provided inputs to prevent XSS or injection.
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True)
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True)

    # Populate the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )

    return invitation_html