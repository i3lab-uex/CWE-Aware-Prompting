import html

# Template for the invitation with placeholders.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h2>{event_title}</h2>
    <p class="date">{event_date}</p>
    <div class="description">
        {event_description}
    </div>
    <div class="notes">
        <strong>Additional Notes:</strong>
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
    Render a sanitized HTML invitation.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain multiple lines).
    event_date : str
        Date of the event.
    additional_notes : str
        Any user‑provided extra notes.

    Returns
    -------
    str
        Sanitized HTML ready for rendering.
    """
    # Escape all user input to prevent XSS and other injection attacks.
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=False).replace("\n", "<br>")

    # Format the invitation using the safe values.
    rendered = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return rendered.strip()