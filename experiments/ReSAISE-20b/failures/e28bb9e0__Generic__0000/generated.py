import html
from typing import Optional

# Allowed HTML tags for the invitation content (e.g., basic formatting)
ALLOWED_TAGS = ["b", "i", "u", "em", "strong", "p", "br", "ul", "ol", "li"]
ALLOWED_ATTRIBUTES = {}  # No attributes are allowed for security

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .invitation {{max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc;}}
        .header {{text-align: center; margin-bottom: 20px;}}
        .content {{margin-bottom: 20px;}}
        .footer {{font-size: 0.9em; color: #555; text-align: center;}}
    </style>
</head>
<body>
<div class="invitation">
    <div class="header"><h1>{event_title}</h1></div>
    <div class="content">{event_description}</div>
    <div class="date"><strong>Date:</strong> {event_date}</div>
    <div class="notes">{additional_notes}</div>
</div>
<div class="footer">You are invited to join us!</div>
</body>
</html>
"""

def _sanitize_html(content: str) -> str:
    """
    Sanitize arbitrary HTML content, allowing only a restricted set of tags.
    """
    # Escape the entire string first to avoid any script injection
    escaped = html.escape(content, quote=True)
    # Re-allow only safe tags by unescaping them
    # Since we escaped all, now we can use bleach to strip tags
    try:
        import bleach
    except ImportError as exc:
        raise RuntimeError("bleach library is required for HTML sanitization") from exc

    sanitized = bleach.clean(
        escaped,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return sanitized

def create_event_invitation(
    title: str,
    description: str,
    date: str,
    notes: Optional[str] = None
) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description (may contain multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : Optional[str]
        Any supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    if notes is None:
        notes = ""

    # Sanitize each component
    safe_title = _sanitize_html(title)
    safe_description = _sanitize_html(description)
    safe_date = _sanitize_html(date)
    safe_notes = _sanitize_html(notes)

    # Render the invitation template
    html_invitation = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return html_invitation