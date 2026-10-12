import html

# Template for the invitation (must not be altered by user input)
INVITATION_FORMAT = """
<div class="invitation">
  <h1>{event_title}</h1>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="description">{event_description}</div>
  <div class="notes"><em>Additional notes:</em> {additional_notes}</div>
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
        Any extra notes from the user.

    Returns
    -------
    str
        Sanitized HTML content ready for safe rendering on a web page.

    Raises
    ------
    ValueError
        If any of the required arguments is not a string.
    """
    # Validate types to avoid accidental injection via non-string objects
    for name, value in [
        ("event_title", event_title),
        ("event_description", event_description),
        ("event_date", event_date),
        ("additional_notes", additional_notes),
    ]:
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")

    # Escape user input to neutralize any HTML/JS injection attempts
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=False).replace("\n", "<br>")

    # Construct the final HTML
    rendered = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return rendered.strip()