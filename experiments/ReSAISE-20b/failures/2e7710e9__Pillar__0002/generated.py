import html

# Template for the invitation.  Placeholders are escaped before insertion.
INVITATION_FORMAT = """
<div class="event-invitation">
  <h2>{event_title}</h2>
  <p class="description">{event_description}</p>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="additional-notes">{additional_notes}</div>
</div>
"""

def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Render a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    event_title : str
        The title of the event.
    event_description : str
        Full description of the event (may contain line breaks).
    event_date : str
        The date of the event.
    additional_notes : str
        Any user‑provided notes about the event.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering on a web page.

    Notes
    -----
    All user supplied data is escaped with `html.escape` to avoid XSS and
    ensure the output is well‑formed HTML.  The function does not perform
    any further validation of dates or content, as that is outside the scope
    of this rendering helper.
    """
    # Escape all user supplied content to prevent injection attacks
    escaped_title = html.escape(event_title, quote=True)
    escaped_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(event_date, quote=True)
    escaped_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    # Format the invitation using the sanitized values
    return INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )