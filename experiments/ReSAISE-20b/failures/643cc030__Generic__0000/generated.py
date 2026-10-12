import html

# Example invitation template – adjust placeholders as needed.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <section style="margin-top: 20px;">
        <h2>Description</h2>
        <p>{event_description}</p>
    </section>
    {additional_notes_section}
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Produce a sanitized HTML event invitation.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description (may contain line breaks).
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string representing the invitation.
    """
    # Escape user-provided content to prevent XSS
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace('\n', '<br>')

    # Include notes only if provided
    additional_notes_section = (
        f"<section style='margin-top: 20px;'><h2>Additional Notes</h2><p>{safe_notes}</p></section>"
        if safe_notes.strip()
        else ""
    )

    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=additional_notes_section
    )
    return invitation_html.strip()