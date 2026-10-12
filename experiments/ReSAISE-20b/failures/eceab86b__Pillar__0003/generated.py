import html
from typing import Final

# Predefined HTML template with placeholders for the invitation components.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .invitation {{border: 2px solid #333; padding: 20px; max-width: 600px; margin: auto;}}
        .event-title {{font-size: 1.8em; margin-bottom: 10px;}}
        .event-date {{color: #555; font-style: italic; margin-bottom: 15px;}}
        .event-description {{margin-bottom: 20px;}}
        .event-notes {{font-weight: bold; color: #d00;}}
    </style>
</head>
<body>
    <div class="invitation">
        <div class="event-title">{event_name}</div>
        <div class="event-date">Date: {date_of_event}</div>
        <div class="event-description">{description_of_event}</div>
        <div class="event-notes">Notes: {notes_for_event}</div>
    </div>
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain multiple lines).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Sanitize all user-provided content to prevent XSS and ensure well‑formed HTML.
    safe_event_name = html.escape(event_name, quote=True)
    # Preserve line breaks in description by converting them to <br> tags.
    safe_description = html.escape(description_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True)

    # Format the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )

    return invitation_html