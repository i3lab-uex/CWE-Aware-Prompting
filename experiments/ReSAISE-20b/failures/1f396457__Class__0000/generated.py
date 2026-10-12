import html

# Pre‑defined HTML template with placeholders for event data.
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
    {additional_notes_block}
</body>
</html>
"""

def generate_event_html(title: str, description: str,
                        date: str, extra_notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may contain newlines).
    date : str
        The date on which the event is scheduled.
    extra_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string that safely renders the event invitation.
    """
    # Escape all user-supplied content to avoid HTML injection (CWE‑74).
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=False).replace('\n', '<br>')

    # Conditionally include the notes block only if provided.
    additional_notes_block = (
        f"<div><strong>Additional Notes:</strong> {safe_notes}</div>"
        if safe_notes.strip()
        else ""
    )

    # Render the final HTML using the template.
    html_output = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_block=additional_notes_block
    )

    return html_output.strip()