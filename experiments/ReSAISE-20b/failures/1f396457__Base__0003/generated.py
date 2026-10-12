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
    <footer>{additional_notes}</footer>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Produce a sanitized HTML representation of an event invitation.

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
        A string of sanitized HTML that safely renders the event invitation.

    Notes
    -----
    All user-supplied content is escaped using html.escape to prevent XSS attacks
    (CWE-79). No other transformations are performed; this function does not alter
    the semantics of the input beyond escaping special HTML characters.
    """
    # Escape user inputs to neutralize potential XSS vectors
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace('\n', '<br>')

    # Format the invitation with sanitized values
    html_content = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )
    return html_content