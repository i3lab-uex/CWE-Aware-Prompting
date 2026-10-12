import html

# Template for the invitation.  The placeholders will be filled with escaped values.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <p class="description">{event_description}</p>
    <p class="date"><strong>Date:</strong> {event_date}</p>
    <div class="notes">{additional_notes}</div>
</div>
"""

def render_event_invitation(event_title: str,
                            event_description: str,
                            event_date: str,
                            additional_notes: str) -> str:
    """
    Render a sanitized HTML event invitation.

    Args:
        event_title: The title of the event.
        event_description: Full description (may contain multiple lines).
        event_date: Date of the event.
        additional_notes: User‑provided notes.

    Returns:
        A string containing safe HTML ready for rendering on a web page.
    """
    # Escape all user input to prevent XSS (CWE‑79)
    safe_title = html.escape(event_title, quote=True)
    safe_description = html.escape(event_description, quote=True).replace('\n', '<br>')
    safe_date = html.escape(event_date, quote=True)
    safe_notes = html.escape(additional_notes, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )