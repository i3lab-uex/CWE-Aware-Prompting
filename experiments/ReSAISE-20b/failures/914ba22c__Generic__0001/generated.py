import html

# Predefined HTML template with placeholders for the event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background:#f5f5f5; padding:10px; text-align:center; }}
        .content {{ margin:20px; }}
        .notes {{ background:#fafafa; padding:10px; border-left:4px solid #ccc; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{event_title}</h1>
        <p><strong>Date:</strong> {event_date}</p>
    </div>
    <div class="content">
        {event_description}
    </div>
    <div class="notes">
        {additional_notes}
    </div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description of the event (may include multiple paragraphs).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-provided content to prevent XSS or injection attacks.
    safe_title = html.escape(title, quote=True)
    # Preserve line breaks in description by converting newlines to <br>
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )