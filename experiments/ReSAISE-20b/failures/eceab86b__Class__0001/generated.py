import html

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_name} Invitation</title>
<style>
    body {{font-family: Arial, sans-serif; margin: 20px;}}
    .invitation {{border: 1px solid #ccc; padding: 20px; border-radius: 5px;}}
    .header {{font-size: 1.5em; margin-bottom: 10px;}}
    .date {{color: #555; margin-bottom: 15px;}}
    .description, .notes {{margin-top: 10px; white-space: pre-wrap;}}
</style>
</head>
<body>
<div class="invitation">
    <div class="header">{event_name}</div>
    <div class="date">Date: {date_of_event}</div>
    <div class="description">{description_of_event}</div>
    {notes_block}
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
        The title of the event.
    description_of_event : str
        Detailed description, may contain newlines and formatting.
    date_of_event : str
        Scheduled date for the event.
    notes_for_event : str
        Additional notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe rendering.
    """
    # Escape all user-supplied content to prevent injection
    esc_event_name = html.escape(event_name, quote=True)
    esc_description = html.escape(description_of_event, quote=True)
    esc_date = html.escape(date_of_event, quote=True)

    # Notes are optional; include only if provided
    if notes_for_event.strip():
        esc_notes = html.escape(notes_for_event, quote=True)
        notes_block = f'<div class="notes"><strong>Notes:</strong><br>{esc_notes}</div>'
    else:
        notes_block = ''

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        event_name=esc_event_name,
        description_of_event=esc_description,
        date_of_event=esc_date,
        notes_block=notes_block
    )