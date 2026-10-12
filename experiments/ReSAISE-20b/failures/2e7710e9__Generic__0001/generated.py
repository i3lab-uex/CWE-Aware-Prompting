import html

# Template for the invitation.  Use double curly braces so that .format() can
# replace them safely without executing any code.
INVITATION_FORMAT = """
<div class="event-invitation">
  <h2>{event_title}</h2>
  <p class="description">{event_description}</p>
  <p class="date"><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
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
        Title of the event.
    event_description : str
        Full description (may contain newlines or other formatting).
    event_date : str
        Date of the event.
    additional_notes : str
        Any user‑provided notes about the event.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Escape all user supplied data to avoid XSS attacks
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=False).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )