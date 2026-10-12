import html

# Predefined HTML template with placeholders for safe formatting.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_name} Invitation</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    .event-title {{ font-size: 2em; font-weight: bold; margin-bottom: 10px; }}
    .event-date {{ color: #555; margin-bottom: 20px; }}
    .event-description, .event-notes {{ white-space: pre-wrap; margin-bottom: 20px; }}
</style>
</head>
<body>
<div class="event-title">{event_name}</div>
<div class="event-date">Date: {date_of_event}</div>
<div class="event-description">{description_of_event}</div>
{notes_block}
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
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        Title of the event.
    description_of_event : str
        Detailed description (may contain newlines).
    date_of_event : str
        Scheduled date of the event.
    notes_for_event : str
        Extra instructions or information.

    Returns
    -------
    str
        A complete HTML document with all user-supplied content escaped.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    # Basic validation
    if not all([event_name, description_of_event, date_of_event]):
        raise ValueError("Event name, description, and date must be provided.")

    # Escape all user-controlled input to prevent XSS
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True)
    safe_date = html.escape(date_of_event, quote=True)

    # Optional notes block: only include if not empty
    if notes_for_event:
        safe_notes = html.escape(notes_for_event, quote=True)
        notes_block = f'<div class="event-notes"><strong>Notes:</strong><br>{safe_notes}</div>'
    else:
        notes_block = ''

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_block=notes_block
    )

    return invitation_html.strip()