import html
from typing import Final

# Pre‑defined HTML template with placeholders
INVITATION_FORMAT: Final[str] = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <div class="description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
</div>
"""

def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str
) -> str:
    """
    Produce a secure HTML representation of an event invitation.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A comprehensive description of the event (may include newlines).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any extra information or instructions supplied by the user.

    Returns
    -------
    str
        A sanitized HTML string that safely renders the event invitation.
    """
    # Helper to escape and preserve line breaks
    def _sanitize(text: str) -> str:
        # Escape HTML special characters to prevent injection
        escaped = html.escape(text, quote=True)
        # Convert newlines to <br> for readability
        return escaped.replace("\n", "<br>")

    sanitized_title = _sanitize(title_of_event)
    sanitized_description = _sanitize(details_of_event)
    sanitized_date = _sanitize(when_event_is)
    sanitized_notes = _sanitize(extra_event_info)

    # Format the invitation using the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=sanitized_title,
        event_description=sanitized_description,
        event_date=sanitized_date,
        additional_notes=sanitized_notes
    )

    return invitation_html.strip()