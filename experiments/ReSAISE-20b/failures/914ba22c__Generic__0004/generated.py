import html

# Predefined HTML template with placeholders for the invitation components.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #2c3e50; }}
        .content {{ margin-top: 1rem; }}
        .notes {{ font-style: italic; color: #7f8c8d; margin-top: 1rem; }}
    </style>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="content">
        {event_description}
    </div>
    <p><strong>Date:</strong> {event_date}</p>
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
        A sanitized HTML string ready for secure display.
    """
    # Escape all user-supplied content to prevent XSS and HTML injection.
    safe_title = html.escape(title, quote=True)
    # For description we preserve basic formatting (like <p>, <br>) but escape other tags.
    # We escape all, then re-allow a limited set of safe tags by replacing them back.
    # This is a simple approach; for production use a library like Bleach.
    safe_description = html.escape(description, quote=True)
    # Allow <p> and <br> tags only.
    for tag in ["<p>", "</p>", "<br>", "<b>", "</b>"]:
        safe_description = safe_description.replace(html.escape(tag), tag)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True)

    # Format the invitation using the template.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html