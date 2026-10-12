import html

# Template for rendering the invitation.
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
        The title of the event.
    event_description : str
        Full description, may contain line breaks or formatting characters.
    event_date : str
        Date string for the event.
    additional_notes : str
        Any user-provided notes.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering.
    """
    # Escape all user-supplied content to prevent XSS and other injection attacks
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace('\n', '<br>')

    # Use a strict format string; no dynamic formatting keys that could be abused
    rendered = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return rendered