import html

# Pre‑defined HTML template with placeholders for the event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 2rem; }}
        h1 {{ color: #333; }}
        .details, .notes {{ margin-top: 1rem; }}
    </style>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="details">
        <p><strong>Date:</strong> {event_date}</p>
        <div>{event_description}</div>
    </div>
    <div class="notes">
        {additional_notes}
    </div>
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Create a secure HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The title or heading of the event.
    e_description : str
        A detailed description of the event. May contain newlines or formatting.
    e_date : str
        The date on which the event is scheduled.
    e_notes : str
        Any additional information or instructions.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering.
    """
    # Escape all user‑supplied content to prevent XSS and other injection attacks.
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace("\n", "<br>")

    # Format the invitation using the template.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html