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
    <footer>{notes}</footer>
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
        A sanitized HTML string ready for safe display in a web page.

    Raises
    ------
    ValueError
        If any of the required arguments are empty strings.
    """
    # Basic validation: ensure no empty values
    for name, value in (("title", title), ("description", description),
                        ("date", date), ("notes", notes)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non‑empty string")

    # Escape all user-provided content to prevent XSS (CWE‑79)
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )