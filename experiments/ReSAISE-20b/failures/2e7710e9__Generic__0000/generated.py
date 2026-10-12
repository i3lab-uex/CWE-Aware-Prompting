import html
from typing import Dict

# Define the invitation format template with placeholders.
INVITATION_FORMAT: str = """
<div class="event-invitation">
  <h2>{event_title}</h2>
  <p class="date">{event_date}</p>
  <div class="description">
    {event_description}
  </div>
  <div class="additional-notes">
    {additional_notes}
  </div>
</div>
"""

def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Render a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_title : str
        The title of the event.
    event_description : str
        Full description of the event (may contain newlines or formatting).
    event_date : str
        The date of the event.
    additional_notes : str
        Any user‑provided notes about the event.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a web page.

    Notes
    -----
    All user‑supplied content is escaped using `html.escape` to prevent XSS.
    The description and notes are wrapped in `<pre>` tags to preserve line breaks
    while still escaping dangerous characters.
    """
    # Helper function to escape and wrap multiline content
    def _escape_and_pre(text: str) -> str:
        escaped = html.escape(text, quote=True)
        # Preserve line breaks by wrapping in <pre>
        return f"<pre>{escaped}</pre>"

    # Prepare a mapping for string formatting
    context: Dict[str, str] = {
        "event_title": html.escape(event_title, quote=True),
        "event_date": html.escape(event_date, quote=True),
        "event_description": _escape_and_pre(event_description),
        "additional_notes": _escape_and_pre(additional_notes),
    }

    # Safely format the template
    sanitized_html = INVITATION_FORMAT.format(**context)

    return sanitized_html.strip()