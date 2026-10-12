import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px;}}
        .event-title {{font-size: 2em; font-weight: bold; margin-bottom: 0.5em;}}
        .event-date {{color: #555; margin-bottom: 1em;}}
        .description, .notes {{margin-bottom: 1.5em; white-space: pre-wrap;}}
    </style>
</head>
<body>
    <div class="event-title">{event_name}</div>
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
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        Title of the event.
    description_of_event : str
        Detailed description, may contain line breaks and formatting.
    date_of_event : str
        Scheduled date for the event.
    notes_for_event : str
        Extra information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe display.
    """
    # Escape all user-controllable inputs
    esc_event_name = html.escape(event_name, quote=True)
    esc_description = html.escape(description_of_event, quote=True)
    esc_date = html.escape(date_of_event, quote=True)

    # Notes are optional; escape only if provided
    if notes_for_event.strip():
        esc_notes = html.escape(notes_for_event, quote=True)
        notes_block = f'<div class="notes"><strong>Notes:</strong><br>{esc_notes}</div>'
    else:
        notes_block = ""

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_name=esc_event_name,
        date_of_event=esc_date,
        description_of_event=esc_description,
        notes_block=notes_block
    )

    return invitation_html