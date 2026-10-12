import html

# Predefined HTML template for the invitation.
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
    {notes_block}
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a secure HTML representation of an event invitation.

    Args:
        title (str): The name or title of the event.
        description (str): A comprehensive description of the event
                           (may contain multiple lines and formatting).
        date (str): The scheduled date for the event.
        notes (str): Extra information or instructions provided by the user.

    Returns:
        str: A sanitized HTML string safe for rendering in a browser.
    """
    # Escape all user-supplied data to prevent XSS (CWE-79)
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Only include the notes block if notes are provided
    notes_block = f"<div><strong>Notes:</strong> {safe_notes}</div>" if safe_notes.strip() else ""

    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes_block=notes_block
    )