import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<div class="event-invite">
  <h1>{title}</h1>
  <p><strong>Date:</strong> {date}</p>
  <div class="description">{description}</div>
  <div class="notes">{notes}</div>
</div>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

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
        A sanitized HTML string ready for safe rendering in a web page.

    Notes
    -----
    The function uses ``html.escape`` to neutralize any potentially malicious content,
    preventing XSS and ensuring compliance with CWE-707 (Improper Neutralization of Structured Data).
    """
    # Escape all user-supplied input to avoid injection attacks.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Format the invitation using the predefined template.
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )