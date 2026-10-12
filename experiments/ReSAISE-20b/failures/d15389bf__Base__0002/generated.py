import html

# Predefined HTML template with placeholders for title, description, date, and notes.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        .event-details, .notes {{ margin-top: 15px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="event-details">
        <p><strong>Date:</strong> {date}</p>
        <div>{description}</div>
    </div>
    <div class="notes">
        {notes}
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
        The name or title of the event.
    description : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date : str
        The scheduled date for the event.
    notes : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Escape all user-controllable input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Format the HTML template with sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )