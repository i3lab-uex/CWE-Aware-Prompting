import html

# Predefined HTML template with placeholders for the event invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 2rem;}}
        .invitation {{border: 1px solid #ddd; padding: 2rem; border-radius: 8px;}}
        h1 {{color: #333;}}
        .date, .notes {{font-style: italic; color: #555;}}
    </style>
</head>
<body>
    <div class="invitation">
        <h1>{title}</h1>
        <p class="date"><strong>Date:</strong> {date}</p>
        <div class="description">{description}</div>
        <p class="notes"><strong>Notes:</strong> {notes}</p>
    </div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

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
        A fully sanitized HTML string ready for safe rendering in a browser.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    for name, value in (("title", title), ("description", description),
                        ("date", date), ("notes", notes)):
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string, got {type(value).__name__}")

    # Escape all user-provided content to prevent XSS
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=False).replace("\n", "<br>")
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Format the invitation using the predefined template
    html_invite = INVITATION_FORMAT.format(
        title=escaped_title,
        description=escaped_description,
        date=escaped_date,
        notes=escaped_notes
    )

    return html_invite