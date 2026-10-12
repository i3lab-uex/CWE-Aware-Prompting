import html

# Example invitation format; in a real application this would be defined elsewhere.
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
    <section>{event_description}</section>
    <footer><em>{additional_notes}</em></footer>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation.

    Parameters
    ----------
    title : str
        The event's title or name.
    description : str
        Detailed description of the event. May contain multiple paragraphs.
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions.

    Returns
    -------
    str
        A sanitized HTML string suitable for safe rendering in a browser.

    Raises
    ------
    ValueError
        If any required argument is empty or not a string.
    """
    # Basic type and emptiness checks
    for name, value in (("title", title), ("description", description),
                        ("date", date), ("notes", notes)):
        if not isinstance(value, str):
            raise ValueError(f"{name!r} must be a string")
        if not value.strip():
            raise ValueError(f"{name!r} cannot be empty")

    # Escape user-provided content to prevent XSS
    escaped = {
        "event_title": html.escape(title, quote=True),
        "event_description": html.escape(description, quote=False).replace("\n", "<br>"),
        "event_date": html.escape(date, quote=True),
        "additional_notes": html.escape(notes, quote=False).replace("\n", "<br>"),
    }

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(**escaped)