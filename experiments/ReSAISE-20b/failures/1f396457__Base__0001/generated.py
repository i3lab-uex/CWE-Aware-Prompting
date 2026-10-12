import html

# Pre‑defined template with placeholders for the invitation parts.
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
    Produce a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        A detailed description that may contain newlines and other formatting.
    date : str
        The scheduled date of the event.
    extra_notes : str
        Any additional user‑supplied information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user‑controlled content to prevent XSS attacks (CWE-79).
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )