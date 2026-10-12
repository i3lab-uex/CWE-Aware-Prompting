import html

# Template for the invitation page.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .invitation {{ border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }}
        h1 {{ color: #2c3e50; }}
        .details, .notes {{ margin-top: 1rem; }}
    </style>
</head>
<body>
    <div class="invitation">
        <h1>{event_title}</h1>
        <div class="details">
            <strong>Date:</strong> {event_date}<br>
            <strong>Description:</strong><br>
            <pre>{event_description}</pre>
        </div>
        {additional_notes_block}
    </div>
</body>
</html>
"""

def render_event_invitation(event_title: str,
                            event_description: str,
                            event_date: str,
                            additional_notes: str) -> str:
    """
    Render a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_title : str
        Title of the event.
    event_description : str
        Full description, may contain newlines and formatting characters.
    event_date : str
        Date of the event.
    additional_notes : str
        Any user-provided notes. If empty, this section is omitted.

    Returns
    -------
    str
        Sanitized HTML content ready for rendering in a browser.
    """
    # Escape all user-provided input to prevent XSS (CWE-79).
    esc_title = html.escape(event_title, quote=True)
    esc_description = html.escape(event_description, quote=False).replace('\n', '\n')
    esc_date = html.escape(event_date, quote=True)
    esc_notes = html.escape(additional_notes, quote=False).replace('\n', '\n')

    if esc_notes.strip():
        notes_block = f"""
        <div class="notes">
            <strong>Additional Notes:</strong><br>
            <pre>{esc_notes}</pre>
        </div>
        """
    else:
        notes_block = ""

    return INVITATION_FORMAT.format(
        event_title=esc_title,
        event_description=esc_description,
        event_date=esc_date,
        additional_notes_block=notes_block
    )