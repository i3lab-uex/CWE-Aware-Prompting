import html

# Template for rendering the invitation.
# Placeholders are marked with `{}` and will be replaced by escaped values.
INVITATION_FORMAT = """
<div class="invitation">
    <h2>{event_title}</h2>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="description">{event_description}</div>
    <div class="notes"><em>Additional Notes:</em> {additional_notes}</div>
</div>
"""

def render_event_invitation(
    event_title: str,
    event_description: str,
    event_date: str,
    additional_notes: str
) -> str:
    """
    Render a sanitized HTML invitation using user-provided data.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description, possibly containing line breaks or other formatting.
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes from the user.

    Returns
    -------
    str
        Sanitized HTML content ready for rendering.
    """
    # Escape all user input to prevent XSS or injection attacks
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    # Format the invitation with escaped values
    html_content = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return html_content.strip()