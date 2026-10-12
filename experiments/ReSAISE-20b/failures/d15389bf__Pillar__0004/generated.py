import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT: str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p><strong>Date:</strong> {date}</p>
    <section>
        <h2>Description</h2>
        <pre>{description}</pre>
    </section>
    {notes_section}
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

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
        A sanitized HTML string ready for safe rendering in a browser.

    Notes
    -----
    All user-provided content is escaped to prevent XSS and other injection attacks.
    The function does not allow arbitrary HTML or script tags in the output.
    """
    # Escape all user input to neutralize any potentially malicious content.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)

    # The notes section is optional; escape it if provided.
    if notes:
        safe_notes = html.escape(notes, quote=True)
        notes_section = f"""
    <section>
        <h2>Additional Notes</h2>
        <p>{safe_notes}</p>
    </section>
"""
    else:
        notes_section = ""

    # Build the final HTML using the predefined template.
    html_output = INVITATION_FORMAT.format(
        title=safe_title,
        date=safe_date,
        description=safe_description,
        notes_section=notes_section
    )

    return html_output.strip()