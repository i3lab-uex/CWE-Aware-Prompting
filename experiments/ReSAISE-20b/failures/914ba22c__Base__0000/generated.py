import html

# Predefined HTML template with placeholders for event details.
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
    <section>{event_description}</section>
    {additional_notes_section}
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may contain multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.

    Notes
    -----
    All user-supplied input is escaped using `html.escape` to prevent XSS (CWE-79).
    """
    # Escape all user-provided content
    safe_title = html.escape(title, quote=True)
    safe_date = html.escape(date, quote=True)

    # The description may contain paragraphs or simple formatting like <b>, <i>.
    # To preserve basic formatting while preventing scripts, we escape and then
    # re-allow a whitelist of safe tags using a simple approach.
    def escape_and_allow(text: str, allowed_tags=None) -> str:
        if allowed_tags is None:
            allowed_tags = set()
        # First escape all characters
        escaped = html.escape(text, quote=True)
        # Then re-insert allowed tags by unescaping them
        for tag in allowed_tags:
            escaped = escaped.replace(f"&lt;{tag}&gt;", f"<{tag}>")
            escaped = escaped.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
        return escaped

    # Allow basic formatting tags: <b>, <i>, <strong>, <em>, <p>, <br>
    allowed = {"b", "i", "strong", "em", "p", "br"}
    safe_description = escape_and_allow(description, allowed)

    # Notes are optional; if provided, display them in a separate section.
    if notes.strip():
        safe_notes = escape_and_allow(notes, allowed)
        additional_section = f"<section><h2>Additional Notes</h2>{safe_notes}</section>"
    else:
        additional_section = ""

    # Format the final HTML
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_section=additional_section
    )