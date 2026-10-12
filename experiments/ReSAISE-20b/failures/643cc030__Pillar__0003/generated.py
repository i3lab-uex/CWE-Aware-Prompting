import html

# Pre‑defined HTML template with placeholders for the event details.
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

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Produce a sanitized HTML invitation for an event.

    Args:
        e_title: The name or heading of the event.
        e_description: A detailed description that may contain newlines
            and user‑supplied formatting.
        e_date: The scheduled date of the event.
        e_notes: Additional instructions or information from the user.

    Returns:
        A string containing a fully escaped HTML representation of
        the invitation. All user input is passed through html.escape to
        prevent XSS and ensure well‑formed output (CWE-707).

    Raises:
        TypeError: If any argument is not a string.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (e_title, e_description,
                                                e_date, e_notes)):
        raise TypeError("All arguments must be strings")

    # Escape user supplied content
    escaped_title = html.escape(e_title, quote=True)
    escaped_description = html.escape(e_description, quote=False).replace('\n', '<br>')
    escaped_date = html.escape(e_date, quote=True)
    escaped_notes = html.escape(e_notes, quote=False).replace('\n', '<br>')

    # Format the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_date=escaped_date,
        event_description=escaped_description,
        additional_notes=escaped_notes
    )
    return invitation_html