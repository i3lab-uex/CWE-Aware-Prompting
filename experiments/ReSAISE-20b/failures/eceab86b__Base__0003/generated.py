import html

# Predefined HTML template with placeholders for the invitation data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .invitation {{ border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }}
        h1 {{ color: #2c3e50; }}
        .details, .notes {{ margin-top: 1rem; }}
    </style>
</head>
<body>
    <div class="invitation">
        <h1>{event_name}</h1>
        <p class="details">{description_of_event}</p>
        <p><strong>Date:</strong> {date_of_event}</p>
        <div class="notes"><strong>Notes:</strong> {notes_for_event}</div>
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
    Generate a sanitized HTML invitation for an event.

    Args:
        event_name: Title of the event.
        description_of_event: Detailed description (may contain newlines or formatting).
        date_of_event: Scheduled date string.
        notes_for_event: Additional instructions or notes.

    Returns:
        A string containing the HTML invitation with all user-provided content escaped
        to prevent XSS attacks (CWE-79).
    """
    # Escape all user-provided content to neutralize HTML special characters.
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True).replace('\n', '<br>')

    # Format the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )
    return invitation_html