import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px;}}
        .header {{background-color:#f4f4f4;padding:10px;border-radius:5px;}}
        .content {{margin-top:15px;}}
        .notes {{font-size:0.9em;color:#555;margin-top:10px;border-left:3px solid #ccc;padding-left:10px;}}
    </style>
</head>
<body>
    <div class="header">
        <h1>{event_title}</h1>
        <p><strong>Date:</strong> {event_date}</p>
    </div>
    <div class="content">
        {event_description}
    </div>
    <div class="notes">
        {additional_notes}
    </div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
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
        Sanitized HTML content for secure display of the event invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise TypeError("All arguments must be of type str")

    # Escape all user-provided content to prevent HTML injection
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace('\n', '<br>')  # preserve line breaks
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace('\n', '<br>')

    # Format the invitation using the predefined template
    html_content = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return html_content