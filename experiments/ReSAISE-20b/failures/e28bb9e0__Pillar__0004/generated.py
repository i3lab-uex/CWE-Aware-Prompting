import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="notes">{additional_notes}</div>
</body>
</html>
"""

def _sanitize_html(text: str) -> str:
    """
    Escape special HTML characters and preserve line breaks by converting
    newline sequences into <br> tags. This mitigates XSS and ensures the output
    is well‑formed HTML.
    """
    # Escape HTML special characters first
    escaped = html.escape(text, quote=True)
    # Convert line breaks to <br> tags
    return escaped.replace("\n", "<br>")

def create_event_invitation(
    title: str,
    description: str,
    date: str,
    notes: str
) -> str:
    """
    Generate a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The event's title or name.
    description : str
        A comprehensive description of the event. May contain multiple paragraphs
        and formatting.
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering in a browser.

    Raises
    ------
    ValueError
        If any required argument is missing or not a string.
    """
    # Basic type checks
    for arg_name, arg_value in (
        ("title", title),
        ("description", description),
        ("date", date),
        ("notes", notes)
    ):
        if not isinstance(arg_value, str):
            raise ValueError(f"{arg_name!r} must be a string")

    # Sanitize each field
    safe_title = _sanitize_html(title)
    safe_description = _sanitize_html(description)
    safe_date = _sanitize_html(date)
    safe_notes = _sanitize_html(notes)

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return invitation_html.strip()