import html

# Pre‑defined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    .invitation {{ border: 1px solid #ccc; padding: 2rem; border-radius: 8px; }}
    .header {{ font-size: 1.5rem; margin-bottom: 1rem; }}
    .description {{ white-space: pre-wrap; margin-bottom: 1rem; }}
    .date, .notes {{ font-style: italic; color: #555; }}
</style>
</head>
<body>
<div class="invitation">
    <div class="header">{event_title}</div>
    <div class="description">{event_description}</div>
    <div class="date">Date: {event_date}</div>
    <div class="notes">{additional_notes}</div>
</div>
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
    Produce a sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The title of the event.
    e_description : str
        A detailed description; may contain newlines or formatting.
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Any additional notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user supplied content to mitigate XSS (CWE‑79).
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True)
    safe_date = html.escape(e_date, quote=True)
    safe_notes = html.escape(e_notes, quote=True)

    # Populate the template with the escaped values.
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )