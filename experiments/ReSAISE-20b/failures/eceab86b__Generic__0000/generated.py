import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<div class="event-invitation">
    <h2>{event_name}</h2>
    <p class="description">{description_of_event}</p>
    <p class="date"><strong>Date:</strong> {date_of_event}</p>
    <div class="notes">{notes_for_event}</div>
</div>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Escape all user-supplied content to prevent XSS
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True).replace("\n", "<br>")

    # Render the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )

    return invitation_html.strip()