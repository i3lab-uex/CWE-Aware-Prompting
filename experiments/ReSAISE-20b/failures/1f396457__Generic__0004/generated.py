import html

# Pre‑defined template containing placeholders that will be replaced safely.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <div class="event-date">{event_date}</div>
    <div class="event-description">{event_description}</div>
    {additional_notes_block}
</div>
"""

def _escape_and_format(text: str) -> str:
    """
    Escape HTML special characters to prevent injection.
    Also collapse excessive whitespace and trim surrounding spaces.
    """
    if text is None:
        return ""
    # Collapse newlines and multiple spaces into single space for consistency
    cleaned = " ".join(text.strip().split())
    return html.escape(cleaned)

def generate_event_html(
    title: str,
    description: str,
    date: str,
    extra_notes: str
) -> str:
    """
    Produce a sanitized HTML string for an event invitation.

    Parameters
    ----------
    title : str
        The heading of the event.
    description : str
        Detailed information about the event. May contain newlines and user formatting.
    date : str
        The scheduled date of the event.
    extra_notes : str
        Optional additional information.

    Returns
    -------
    str
        A safe HTML representation of the invitation.
    """
    # Escape all user‑supplied content
    escaped_title = _escape_and_format(title)
    escaped_description = _escape_and_format(description).replace("\n", "<br>")
    escaped_date = _escape_and_format(date)

    # Render optional notes only if provided
    if extra_notes:
        escaped_notes = _escape_and_format(extra_notes).replace("\n", "<br>")
        notes_block = f'<div class="event-notes">{escaped_notes}</div>'
    else:
        notes_block = ""

    # Substitute placeholders
    html_output = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_date=escaped_date,
        event_description=escaped_description,
        additional_notes_block=notes_block
    )
    return html_output.strip()