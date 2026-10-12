import html

# Template for the invitation HTML.  The placeholders are simple Python format keys.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h1>{event_title}</h1>
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
        Full description (may contain multiple lines).
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes provided by the user.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Escape all user-provided content to prevent XSS and other injection attacks
    escaped_title = html.escape(event_title, quote=True)
    # Preserve line breaks in description by converting \n to <br>
    escaped_description = html.escape(event_description, quote=True).replace('\n', '<br>')
    escaped_date = html.escape(event_date, quote=True)
    escaped_notes = html.escape(additional_notes, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )