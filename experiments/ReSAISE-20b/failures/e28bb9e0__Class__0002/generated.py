import html

# Predefined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 2rem;}}
        .invitation {{border: 1px solid #ccc; padding: 2rem; border-radius: 8px;}}
        .title {{font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;}}
        .date {{color: #555; margin-bottom: 1.5rem;}}
        .description, .notes {{margin-bottom: 1rem; white-space: pre-wrap;}}
    </style>
</head>
<body>
<div class="invitation">
    <div class="title">{event_title}</div>
    <div class="date">Date: {event_date}</div>
    <div class="description">{event_description}</div>
    <div class="notes">{additional_notes}</div>
</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

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
    # Escape all user-supplied content to neutralize any HTML special characters
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True)

    # Render the invitation using the sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )