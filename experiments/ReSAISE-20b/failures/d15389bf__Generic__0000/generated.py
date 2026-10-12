import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .event-title {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .event-date {{ color: #555; margin-bottom: 1rem; }}
        .description {{ white-space: pre-wrap; margin-bottom: 1rem; }}
        .notes {{ font-style: italic; color: #333; }}
    </style>
</head>
<body>
    <div class="event-title">{title}</div>
    <div class="event-date">Date: {date}</div>
    <div class="description">{description}</div>
    <div class="notes">Notes: {notes}</div>
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
        A string containing sanitized HTML for safely displaying the event invitation.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    """
    # Validate argument types
    for arg, name in zip((title, description, date, notes),
                         ("title", "description", "date", "notes")):
        if not isinstance(arg, str):
            raise TypeError(f"Argument '{name}' must be a string")

    # Escape all user-provided content to prevent XSS
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=True)
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=True)

    # Format the invitation
    return INVITATION_FORMAT.format(
        title=escaped_title,
        description=escaped_description,
        date=escaped_date,
        notes=escaped_notes
    )