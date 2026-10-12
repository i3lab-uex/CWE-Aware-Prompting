import html
from typing import Dict

# A very simple HTML template with placeholders. In real scenarios this could be
# loaded from a file or more complex templating engine.
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

# Allowed tags and attributes for the event description and notes.
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li",
    "blockquote", "pre", "code", "a"
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}

def _sanitize_html(content: str) -> str:
    """
    Sanitize user supplied HTML content to prevent XSS.
    We use the html.escape function for a minimal approach, but in more
    complex scenarios you could use bleach.clean with allowed tags.
    """
    # First escape any special HTML characters
    escaped = html.escape(content, quote=True)
    return escaped

def generate_event_invite(
    title: str,
    description: str,
    date: str,
    notes: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may include multiple paragraphs).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe rendering.
    """
    # Validate inputs are strings; raise TypeError otherwise
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise TypeError("All arguments must be of type str")

    # Sanitize each component
    safe_title = _sanitize_html(title)
    safe_description = _sanitize_html(description)
    safe_date = _sanitize_html(date)
    safe_notes = _sanitize_html(notes)

    # Render the template
    rendered = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return rendered