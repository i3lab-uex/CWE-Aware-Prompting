import html

# Predefined HTML template with placeholders for title, description, date, and notes.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p><strong>Date:</strong> {date}</p>
    <div>{description}</div>
    <hr>
    <aside>{notes}</aside>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a sanitized HTML representation of an event invitation.

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
        Sanitized HTML string safe for rendering in a web page.

    Notes
    -----
    All user-provided inputs are escaped using :func:`html.escape` to mitigate
    cross‑site scripting (CWE‑79) by neutralizing special HTML characters.
    """
    # Escape all user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Format the invitation using the sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )