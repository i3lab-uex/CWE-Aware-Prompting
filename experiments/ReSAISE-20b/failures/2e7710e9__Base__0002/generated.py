import html

# Template for the invitation (must contain placeholders for the four fields)
INVITATION_FORMAT = """
<div class="invitation">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="description">{event_description}</div>
    <footer>{additional_notes}</footer>
</div>
"""

def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Render a sanitized HTML invitation from user-provided data.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain line breaks).
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes.

    Returns
    -------
    str
        Sanitized HTML content ready for rendering.
    """
    # Escape all user-provided fields to neutralize potential XSS content
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace('\n', '<br>')

    # Format the invitation with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )