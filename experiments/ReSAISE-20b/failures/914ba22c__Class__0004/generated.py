import html

# Predefined HTML template with placeholders for the event details.
INVITATION_FORMAT = """
<div class="event-invite">
  <h1>{event_title}</h1>
  <div class="description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
</div>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may include multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        A string containing sanitized HTML for secure display of the event invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise TypeError("All arguments must be strings")

    # Escape all user-provided content to neutralize HTML injection
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=True).replace('\n', '<br>')
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=True).replace('\n', '<br>')

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )