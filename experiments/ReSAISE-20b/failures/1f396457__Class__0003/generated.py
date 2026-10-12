import html

# Pre‑defined HTML template with placeholders for event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
    .event {{ border: 1px solid #ccc; padding: 20px; margin: 20px auto; max-width: 600px; }}
    .event h1 {{ margin-top: 0; }}
</style>
</head>
<body>
<div class="event">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    {additional_notes_section}
</div>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        An extensive description of the event (may include multiple lines).
    date : str
        The date on which the event is scheduled.
    extra_notes : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string that safely renders the event invitation.
    """
    # Escape all user-supplied content to prevent HTML injection (CWE‑74).
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace('\n', '<br>')

    # Conditionally include the notes section only if provided.
    if safe_notes.strip():
        additional_notes_section = f"<div><strong>Additional Notes:</strong> {safe_notes}</div>"
    else:
        additional_notes_section = ""

    # Populate the template with sanitized values.
    html_content = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_section=additional_notes_section
    )
    return html_content