import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family:Arial, sans-serif; line-height:1.6;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    {additional_notes_block}
</body>
</html>
"""

def create_event_invitation(
    e_title: str,
    e_description: str,
    e_date: str,
    e_notes: str
) -> str:
    """
    Generate a sanitized HTML invitation.

    Parameters:
        e_title (str): The event title.
        e_description (str): Full description of the event. May contain newlines or formatting markup
                             that will be escaped to avoid injection.
        e_date (str): The scheduled date of the event.
        e_notes (str): Additional notes or instructions. Escaped for safety.

    Returns:
        str: A complete, safe HTML string ready to be sent or displayed.
    """
    # Escape all user-supplied content to prevent XSS and other injection attacks.
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True).replace("\n", "<br>")

    # Conditionally include the notes block only if notes are provided.
    additional_notes_block = (
        f"<div><strong>Additional Notes:</strong><br>{safe_notes}</div>"
        if safe_notes.strip()
        else ""
    )

    # Render the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_block=additional_notes_block
    )

    return invitation_html