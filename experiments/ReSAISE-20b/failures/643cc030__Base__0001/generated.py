import html

# Pre‑defined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 2rem;}}
        .invitation {{border: 1px solid #ccc; padding: 1rem; border-radius: 8px;}}
        h1 {{color: #2c3e50;}}
        .date {{font-weight: bold; margin-top: 0.5rem;}}
        .notes {{margin-top: 1rem; color: #555;}}
    </style>
</head>
<body>
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="date">{event_date}</div>
    <p>{event_description}</p>
    {additional_notes}
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
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The title of the event.
    e_description : str
        A detailed description that may contain line breaks or user formatting.
    e_date : str
        The date of the event.
    e_notes : str
        Any supplementary notes or instructions.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user input to prevent XSS (CWE‑79).
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(e_date, quote=True)
    # If notes are provided, escape and wrap them in a paragraph.
    if e_notes:
        safe_notes = f"<p class=\"notes\">{html.escape(e_notes, quote=True).replace('\n', '<br>')}</p>"
    else:
        safe_notes = ""

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )