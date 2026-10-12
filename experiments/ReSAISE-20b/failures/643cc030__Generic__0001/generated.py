import html

# Predefined HTML template with placeholders
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
    <section style="margin-top: 1em;">
        {event_description}
    </section>
    <footer style="margin-top: 2em; font-size: .9em;">
        {additional_notes}
    </footer>
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Generate a sanitized HTML invitation.

    Parameters
    ----------
    e_title : str
        Title of the event.
    e_description : str
        Full description (may contain line breaks or simple markup).
    e_date : str
        Date of the event.
    e_notes : str
        Extra notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in browsers.
    """
    # Escape all user-supplied content to prevent XSS
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )