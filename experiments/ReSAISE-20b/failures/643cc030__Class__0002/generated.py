import html

# Pre‑defined HTML template with placeholders
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
    <section>
        <h2>Description</h2>
        <pre style="background:#f9f9f9; padding:10px; border-radius:5px;">{event_description}</pre>
    </section>
    <section>
        <h2>Additional Notes</h2>
        <pre style="background:#f0f0f0; padding:10px; border-radius:5px;">{additional_notes}</pre>
    </section>
</body>
</html>
"""

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Generate a secure HTML invitation from user input.

    All user-supplied content is escaped to prevent HTML injection.
    The function returns a complete HTML document that can be safely
    embedded or displayed in a browser.

    Parameters:
        e_title (str): The event title.
        e_description (str): Detailed description of the event.
        e_date (str): Scheduled date of the event.
        e_notes (str): Any extra instructions or notes.

    Returns:
        str: Sanitized HTML invitation.
    """
    # Escape all user-provided content
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=False)
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=False)

    # Render the invitation using the template
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )