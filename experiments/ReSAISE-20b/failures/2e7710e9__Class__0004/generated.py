import html

# Template for the invitation.  The placeholders will be replaced with sanitized values.
INVITATION_FORMAT = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <div class="description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
</div>
"""

def render_event_invitation(event_title: str,
                            event_description: str,
                            event_date: str,
                            additional_notes: str) -> str:
    """
    Render a sanitized HTML invitation from user‑provided data.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain line breaks or formatting characters).
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes supplied by the user.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Escape all user inputs to neutralize special characters that could
    # break HTML structure or introduce XSS vulnerabilities.
    safe_title = html.escape(event_title, quote=True)
    # Preserve line breaks in the description by converting \n to <br>.
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )