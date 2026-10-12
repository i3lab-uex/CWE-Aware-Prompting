import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .invitation {{ border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }}
        .event-title {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .event-date {{ color: #555; margin-bottom: 1rem; }}
        .description, .notes {{ white-space: pre-wrap; margin-bottom: 1rem; }}
    </style>
</head>
<body>
<div class="invitation">
    <div class="event-title">{event_name}</div>
    <div class="event-date">Date: {date_of_event}</div>
    <div class="description">{description_of_event}</div>
    {notes_block}
</div>
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
    Generate a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain newlines).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML ready for safe rendering.
    """
    # Escape all user-provided content to neutralize any HTML or script injection attempts.
    escaped_event_name = html.escape(event_name, quote=True)
    escaped_description = html.escape(description_of_event, quote=True)
    escaped_date = html.escape(date_of_event, quote=True)
    escaped_notes = html.escape(notes_for_event, quote=True)

    # Conditionally include the notes block only if notes are provided.
    notes_block = ""
    if escaped_notes.strip():
        notes_block = f'<div class="notes"><strong>Notes:</strong> {escaped_notes}</div>'

    # Format the final HTML using the sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_name=escaped_event_name,
        date_of_event=escaped_date,
        description_of_event=escaped_description,
        notes_block=notes_block
    )

    return invitation_html