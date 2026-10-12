import html
from typing import Final

# Predefined HTML template with placeholders for the event details.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="description">
        {event_description}
    </div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="notes">
        {additional_notes}
    </div>
</body>
</html>
"""

def _sanitize_html(text: str) -> str:
    """
    Escape HTML special characters to prevent XSS.
    The function also removes leading/trailing whitespace and normalizes newlines.
    """
    # Strip surrounding whitespace
    text = text.strip()
    # Replace multiple consecutive newlines with a single one
    text = "\n".join(line.strip() for line in text.splitlines())
    # Escape HTML
    return html.escape(text, quote=True)

def prepare_event_details(
    headline: str,
    summary: str,
    scheduled_date: str,
    additional_info: str
) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Args:
        headline: The title or name of the event.
        summary: A comprehensive description of the event (may include multiple paragraphs).
        scheduled_date: The scheduled date of the event.
        additional_info: Any supplementary information or instructions.

    Returns:
        A string containing sanitized HTML for secure display of the event invitation.
    """
    # Sanitize each component
    safe_title = _sanitize_html(headline)
    safe_summary = _sanitize_html(summary).replace("\n", "<br>")
    safe_date = _sanitize_html(scheduled_date)
    safe_notes = _sanitize_html(additional_info).replace("\n", "<br>")

    # Format the HTML using the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return invitation_html