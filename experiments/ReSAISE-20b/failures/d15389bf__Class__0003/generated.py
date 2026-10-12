import html

# Predefined HTML template with placeholders for the event invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
        h1 {{ color: #2c3e50; }}
        .date {{ font-weight: bold; margin-top: 10px; }}
        .notes {{ background-color: #f9f9f9; padding: 10px; margin-top: 15px; border-left: 4px solid #3498db; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{title}</h1>
    <div class="description">{description}</div>
    <div class="date">Date: {date}</div>
    {notes_block}
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
        A string containing sanitized HTML for safely displaying the event invitation.

    Raises
    ------
    ValueError
        If any of the required arguments are empty strings.
    """
    # Basic validation: ensure mandatory fields are provided
    if not title.strip():
        raise ValueError("Title cannot be empty.")
    if not description.strip():
        raise ValueError("Description cannot be empty.")
    if not date.strip():
        raise ValueError("Date cannot be empty.")

    # Escape user-provided content to prevent HTML injection (CWE-74)
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)

    # Notes are optional; if provided, escape and wrap in a styled div
    notes_block = ""
    if notes.strip():
        safe_notes = html.escape(notes, quote=False).replace("\n", "<br>")
        notes_block = f'<div class="notes">{safe_notes}</div>'

    # Render the final HTML using the predefined template
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes_block=notes_block
    )