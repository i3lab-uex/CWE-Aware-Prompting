import html

# Template for the invitation, using Python's format syntax.
INVITATION_FORMAT = """
<div class="invitation">
  <h2>{event_title}</h2>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="description">{event_description}</div>
  {additional_notes_block}
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
        The title of the event.
    event_description : str
        Full description, may contain multiple lines.
    event_date : str
        Date of the event.
    additional_notes : str
        Any extra notes.

    Returns
    -------
    str
        Sanitized HTML content ready for rendering.
    """
    # Escape all user input to avoid XSS or malformed HTML
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    # Conditionally include the notes block if provided
    notes_block = f'<p class="notes"><strong>Notes:</strong> {safe_notes}</p>' if safe_notes.strip() else ''

    # Build the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_block=notes_block
    )

    return invitation_html.strip()