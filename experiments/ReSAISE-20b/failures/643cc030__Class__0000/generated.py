import html

# Pre‑defined HTML template with placeholders for the invitation data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family:Arial,Helvetica,sans-serif;line-height:1.6;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div style="margin-top:1em;">
        {event_description}
    </div>
    {additional_notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Construct a safe HTML invitation using the provided event details.

    Parameters
    ----------
    e_title : str
        Title of the event.
    e_description : str
        Full description (may contain line breaks).
    e_date : str
        Date string for the event.
    e_notes : str
        Additional notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for rendering.
    """
    # Escape all user supplied content to neutralize any malicious markup
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace('\n', '<br>')

    # Only include the notes section if any content is provided
    additional_notes_section = (
        f"<div style='margin-top:1em;'><strong>Notes:</strong><br>{safe_notes}</div>"
        if safe_notes.strip()
        else ""
    )

    # Render the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=additional_notes_section
    )

    return invitation_html