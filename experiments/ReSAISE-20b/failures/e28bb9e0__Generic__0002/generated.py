import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <div class="description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="notes">{additional_notes}</div>
</div>
"""

def create_event_invitation(title: str, description: str,
                            date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

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
        Sanitized HTML string suitable for safe rendering in a web page.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    # Basic validation
    if not all(isinstance(arg, str) and arg.strip() for arg in (title, description, date)):
        raise ValueError("Title, description, and date must be non-empty strings.")

    # Escape all user-supplied content to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes or "", quote=False).replace("\n", "<br>")

    # Render the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html.strip()