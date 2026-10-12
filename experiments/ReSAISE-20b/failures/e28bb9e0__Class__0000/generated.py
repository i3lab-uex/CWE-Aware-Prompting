import html

# Predefined HTML template with placeholders for event data.
INVITATION_FORMAT = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <div class="description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
</div>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description of the event (may include multiple paragraphs and formatting).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for display.
    """
    # Sanitize each user-provided field to neutralize any HTML or script injection.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True)

    # Use a mapping for format_map to avoid accidental string interpolation of user data.
    invitation = INVITATION_FORMAT.format_map({
        "event_title": safe_title,
        "event_description": safe_description,
        "event_date": safe_date,
        "additional_notes": safe_notes
    })

    return invitation.strip()