import html
from string import Template

# Pre‑defined template with placeholders for the invitation components.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Invitation – ${event_title}</title>
</head>
<body>
    <h1>${event_title}</h1>
    <p><strong>Date:</strong> ${event_date}</p>
    <section>
        <h2>Description</h2>
        <div>${event_description}</div>
    </section>
    ${additional_notes_section}
</body>
</html>
"""

def _escape_and_prepare(text: str) -> str:
    """
    Escape all HTML special characters to neutralise potential XSS payloads.
    Preserve newlines by converting them to <br> tags for display purposes.
    """
    escaped = html.escape(text, quote=True)
    # Convert newlines to <br> for readability
    return escaped.replace('\n', '<br>')

def generate_event_html(title: str, description: str, date: str, extra_notes: str) -> str:
    """
    Create a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The heading of the event.
    description : str
        A detailed description (may contain newlines).
    date : str
        The scheduled date of the event.
    extra_notes : str
        Optional user‑supplied notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe rendering.
    """
    # Sanitize all user‑supplied input
    safe_title = _escape_and_prepare(title)
    safe_description = _escape_and_prepare(description)
    safe_date = _escape_and_prepare(date)

    # Prepare the notes section only if content is provided
    if extra_notes.strip():
        safe_notes = _escape_and_prepare(extra_notes)
        notes_section = f"""
<section>
    <h2>Additional Notes</h2>
    <div>{safe_notes}</div>
</section>
"""
    else:
        notes_section = ""

    template = Template(INVITATION_FORMAT)
    return template.substitute(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=notes_section
    )