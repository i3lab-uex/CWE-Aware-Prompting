import html

# Template for the invitation (simple HTML structure)
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
        Full description (may contain line breaks).
    event_date : str
        Date of the event.
    additional_notes : str
        Any user-provided notes.

    Returns
    -------
    str
        Sanitized HTML ready for rendering on a web page.
    """
    # Escape all user-provided content to avoid injection (CWE-74)
    safe_title = html.escape(event_title, quote=True)
    # Preserve line breaks in description by converting newlines to <br>
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )