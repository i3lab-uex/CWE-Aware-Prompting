import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_name} Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
        h1 {{ color: #333; }}
        .details, .notes {{ margin-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_name}</h1>
    <div class="details">
        <strong>Date:</strong> {date_of_event}<br><br>
        <p>{description_of_event}</p>
    </div>
    <div class="notes">
        <strong>Notes:</strong><br>
        <p>{notes_for_event}</p>
    </div>
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
    Generates a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The title of the event.
    description_of_event : str
        Detailed description (may contain line breaks).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Additional information or instructions.

    Returns
    -------
    str
        A string containing the sanitized HTML invitation.
    """
    # Escape all user-controlled input to prevent XSS (CWE-79)
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True).replace("\n", "<br>")

    return INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )