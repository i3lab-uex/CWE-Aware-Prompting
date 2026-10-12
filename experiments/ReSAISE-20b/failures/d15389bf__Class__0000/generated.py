import html

# Predefined HTML template with placeholders for title, description, date and notes.
INVITATION_FORMAT = """
<div class="event-invite">
    <h1>{title}</h1>
    <div class="description">{description}</div>
    <p><strong>Date:</strong> {date}</p>
    <p class="notes">{notes}</p>
</div>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The name or title of the event.
    description : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date : str
        The scheduled date for the event.
    notes : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-provided input to prevent injection attacks (CWE-74)
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Format the invitation using the sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )