import html

# Template for the invitation (HTML). Placeholders are marked with {placeholder}.
INVITATION_FORMAT: str = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="description">{event_description}</div>
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
    Render a sanitized HTML invitation.

    All user supplied text is escaped to prevent XSS and other injection
    vulnerabilities (CWE‑74).  The function returns a complete HTML fragment
    that can be safely inserted into a page.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description (may contain line breaks).
    event_date : str
        Date of the event.
    additional_notes : str
        Any user‑provided notes.

    Returns
    -------
    str
        Sanitized HTML content for the invitation.
    """
    # Escape all user provided fields to neutralize special characters
    escaped_title = html.escape(event_title, quote=True)
    escaped_description = html.escape(event_description, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(event_date, quote=True)
    escaped_notes = html.escape(additional_notes, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )