import html

# Pre‑defined HTML template with placeholders.
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
    {additional_notes_section}
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Create a secure HTML invitation string.

    Parameters
    ----------
    title : str
        The event's title or heading.
    description : str
        A potentially multi‑line description of the event.
    date : str
        The scheduled date of the event.
    extra_notes : str
        Optional additional information or instructions.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering.
    """
    # Escape all user‑supplied content to avoid XSS and HTML injection.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=False).replace('\n', '<br>')

    # Render the notes section only if there are any notes.
    if safe_notes.strip():
        additional_section = f'<p><strong>Additional Notes:</strong> {safe_notes}</p>'
    else:
        additional_section = ''

    # Format the final HTML using the template.
    html_output = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_section=additional_section
    )
    return html_output