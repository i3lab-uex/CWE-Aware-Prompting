import html

# Template for the invitation.  Placeholders use Python format syntax.
INVITATION_FORMAT = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <p class="date">{event_date}</p>
  <div class="description">
    {event_description}
  </div>
  <div class="notes">
    {additional_notes}
  </div>
</div>
"""

def render_event_invitation(event_title: str,
                            event_description: str,
                            event_date: str,
                            additional_notes: str) -> str:
    """
    Render a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_title : str
        The title of the event.
    event_description : str
        Full description (may contain line breaks).
    event_date : str
        The date of the event.
    additional_notes : str
        Any extra notes provided by the user.

    Returns
    -------
    str
        A string containing safe HTML ready for rendering.
    """
    # Escape all user-supplied input to prevent XSS
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )