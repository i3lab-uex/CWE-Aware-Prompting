import html

# Predefined HTML template with placeholders for the invitation data.
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
    <footer>{additional_notes}</footer>
</body>
</html>
"""

def create_event_invitation(e_title: str,
                            e_description: str,
                            e_date: str,
                            e_notes: str) -> str:
    """
    Generate a sanitized HTML invitation string.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description that may contain line breaks or formatting.
    e_date : str
        The date on which the event is scheduled.
    e_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user-supplied data to neutralize potential XSS vectors
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace("\n", "<br>")

    # Format the invitation using the safe values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )