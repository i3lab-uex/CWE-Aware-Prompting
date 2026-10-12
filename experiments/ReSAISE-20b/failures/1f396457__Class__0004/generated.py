import html
from typing import Final

# Pre‑defined HTML template with placeholders.
INVITATION_FORMAT: Final[str] = """
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
    <hr>
    <footer>{additional_notes}</footer>
</body>
</html>
"""

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Generate a secure HTML invitation string.

    All user supplied strings are escaped to prevent XSS or template injection.
    """
    # Escape all external inputs
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(extra_notes, quote=True).replace('\n', '<br>')

    # Format the template safely
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )