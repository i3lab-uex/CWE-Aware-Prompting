import html

# Pre‑defined HTML template with placeholders
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
        A sanitized HTML string containing the event invitation.
    """
    # Escape all user‑supplied content to prevent XSS and other injection attacks
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=False).replace("\n", "<br>")

    # Build the additional notes section only if provided
    additional_notes_section = (
        f"<div><strong>Additional Notes:</strong><br>{safe_notes}</div>"
        if safe_notes.strip()
        else ""
    )

    # Populate the template
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=additional_notes_section
    )