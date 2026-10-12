import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px;}}
        .header {{background-color:#f4f4f4;padding:10px;border-radius:5px;margin-bottom:15px;}}
        .section {{margin-bottom:10px;}}
        .label {{font-weight:bold;color:#333;}}
    </style>
</head>
<body>
    <div class="header">
        <h1>{event_name}</h1>
    </div>
    <div class="section">
        <span class="label">Description:</span><br>
        <pre>{description_of_event}</pre>
    </div>
    <div class="section">
        <span class="label">Date:</span> {date_of_event}
    </div>
    <div class="section">
        <span class="label">Notes:</span><br>
        <pre>{notes_for_event}</pre>
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
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The title of the event.
    description_of_event : str
        Detailed description (may contain newlines).
    date_of_event : str
        The scheduled date of the event.
    notes_for_event : str
        Additional instructions or information.

    Returns
    -------
    str
        A fully escaped HTML string ready for safe rendering.
    """
    # Escape all user-provided content to prevent XSS or injection attacks
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True)
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True)

    # Populate the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )

    return invitation_html