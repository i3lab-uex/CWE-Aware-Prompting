import html

# Pre‑defined template with placeholders that will be safely substituted.
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
    <hr/>
    <footer>{additional_notes}</footer>
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
        A detailed, potentially multi‑line description of the event.
    date : str
        The scheduled date for the event.
    extra_notes : str
        Additional user supplied information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in browsers.
    """
    # Escape all user supplied content to avoid injection attacks (CWE‑74).
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace("\n", "<br>")

    # Use format_map to insert the sanitized values into the template.
    invitation = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation