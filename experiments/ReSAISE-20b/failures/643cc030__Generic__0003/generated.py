import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    {additional_notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Produce a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    e_title : str
        Title or heading of the event.
    e_description : str
        Full description, may contain line breaks and formatting.
    e_date : str
        Date of the event.
    e_notes : str
        Extra information or instructions.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering.
    """
    # Escape all user-supplied content to prevent XSS
    esc_title = html.escape(e_title, quote=True)
    esc_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    esc_date = html.escape(e_date, quote=True)
    esc_notes = html.escape(e_notes, quote=True).replace("\n", "<br>")

    # Build notes section only if provided
    notes_section = (
        f"<div><strong>Additional Notes:</strong><br>{esc_notes}</div>"
        if esc_notes.strip()
        else ""
    )

    # Format the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=esc_title,
        event_description=esc_description,
        event_date=esc_date,
        additional_notes_section=notes_section
    )

    return invitation_html.strip()