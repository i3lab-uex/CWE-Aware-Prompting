import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .container {{max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd;}}
        h1 {{color: #333;}}
        .date {{font-weight: bold; margin-top: 10px;}}
        .notes {{margin-top: 20px; font-style: italic; color: #555;}}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <div class="date">Date: {event_date}</div>
    <div class="notes">{additional_notes}</div>
</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description (may contain multiple paragraphs).
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-provided content to prevent XSS or other injection attacks.
    safe_title = html.escape(title, quote=True)
    # Preserve line breaks in the description by converting newlines to <br> tags.
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True).replace("\n", "<br>")

    # Populate the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html