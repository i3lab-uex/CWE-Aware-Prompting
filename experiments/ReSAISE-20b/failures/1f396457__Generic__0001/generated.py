import html

# Example invitation template; in real usage this would be defined elsewhere.
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

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Generate a safe HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may include multiple lines and formatting).
    date : str
        The date on which the event is scheduled.
    extra_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string containing the invitation.
    """
    # Escape all user-supplied content to avoid XSS or HTML injection
    esc_title = html.escape(title, quote=True)
    esc_description = html.escape(description, quote=False).replace('\n', '<br>')
    esc_date = html.escape(date, quote=True)
    esc_notes = html.escape(extra_notes, quote=False).replace('\n', '<br>')

    # Conditionally include the notes block only if there are notes
    additional_notes_block = f"<p><strong>Additional Notes:</strong> {esc_notes}</p>" if esc_notes.strip() else ""

    return INVITATION_FORMAT.format(
        event_title=esc_title,
        event_date=esc_date,
        event_description=esc_description,
        additional_notes_block=additional_notes_block
    )