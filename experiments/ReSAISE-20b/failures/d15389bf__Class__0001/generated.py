import html

# Predefined HTML template with placeholders for title, description, date and notes.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 2rem;}}
        h1 {{color: #333;}}
        .content {{margin-top: 1rem;}}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        <p><strong>Date:</strong> {date}</p>
        <h2>Description</h2>
        <pre>{description}</pre>
        {notes_block}
    </div>
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
        A sanitized HTML string suitable for safe display.
    """
    # Escape all user-supplied content to neutralize any HTML or script injection
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)

    # Notes are optional; include them only if provided
    if notes:
        safe_notes = html.escape(notes, quote=True)
        notes_block = f"<h2>Additional Notes</h2>\n<pre>{safe_notes}</pre>"
    else:
        notes_block = ""

    # Populate the template with sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes_block=notes_block
    )