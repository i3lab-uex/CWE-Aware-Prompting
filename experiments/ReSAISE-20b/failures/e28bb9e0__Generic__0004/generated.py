import html

# Predefined HTML template with placeholders for the event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .event-title {{font-size: 2em; margin-bottom: 0.5em;}}
        .event-date {{color: #555; margin-bottom: 1em;}}
        .notes {{font-style: italic; color: #333; margin-top: 1em;}}
    </style>
</head>
<body>
    <div class="event">
        <h1 class="event-title">{event_title}</h1>
        <div class="event-date"><strong>Date:</strong> {event_date}</div>
        <div class="event-description">{event_description}</div>
        {notes_block}
    </div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

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
        A sanitized HTML string suitable for secure display.
    """
    # Escape all user-provided content to prevent XSS or injection attacks
    safe_title = html.escape(title, quote=True)
    # Preserve basic line breaks in description by converting newlines to <br>
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)

    # Optional notes block: include only if non-empty after stripping whitespace
    if notes and notes.strip():
        safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")
        notes_block = f'<div class="notes"><strong>Notes:</strong> {safe_notes}</div>'
    else:
        notes_block = ""

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        notes_block=notes_block
    )
    return invitation_html