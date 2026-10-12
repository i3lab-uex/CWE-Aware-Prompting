import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f8ff; padding: 10px; border-radius: 5px; }}
        .content {{ margin-top: 15px; }}
        .notes {{ margin-top: 20px; font-style: italic; color: #555; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{event_name}</h1>
        <p><strong>Date:</strong> {date_of_event}</p>
    </div>
    <div class="content">
        {description_of_event}
    </div>
    <div class="notes">
        {notes_for_event}
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

    Parameters
    ----------
    event_name : str
        The title of the event.
    description_of_event : str
        A detailed description (may contain newlines).
    date_of_event : str
        The scheduled date.
    notes_for_event : str
        Additional instructions or information.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe rendering.
    """
    # Escape all user-supplied content to neutralize special characters.
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