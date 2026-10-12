import html

# Predefined HTML template with placeholders.
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
    <footer><small>{additional_notes}</small></footer>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

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
        A string containing sanitized HTML that safely renders the event invitation.

    Notes
    -----
    All user-provided content is escaped using html.escape to mitigate XSS (CWE-79).
    """
    # Escape all user-provided content
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace("\n", "<br>")

    # Format the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )