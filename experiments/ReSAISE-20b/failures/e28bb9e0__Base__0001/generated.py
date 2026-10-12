import html

# Predefined HTML template with placeholders for event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6;}}
        .container {{max-width: 600px; margin: auto; padding: 20px;}}
        h1 {{color: #2c3e50;}}
        .date {{font-weight: bold; margin-top: 10px;}}
        .notes {{margin-top: 20px; color: #555; font-style: italic;}}
    </style>
</head>
<body>
<div class="container">
    <h1>{event_title}</h1>
    <div class="date">Date: {event_date}</div>
    <hr/>
    <div class="description">{event_description}</div>
    {additional_notes}
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
        Title of the event.
    description : str
        Detailed description, may contain multiple paragraphs.
    date : str
        Scheduled date of the event.
    notes : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe rendering in a browser.

    Notes
    -----
    All user-provided content is escaped using `html.escape` to mitigate XSS
    (CWE-79). Newline characters in the description are converted to <br>
    tags so that formatting is preserved without allowing raw HTML.
    """
    # Escape all user input to neutralize potential XSS vectors
    safe_title = html.escape(title, quote=True)
    safe_date = html.escape(date, quote=True)

    # Convert newlines to <br> for the description while escaping other content
    safe_description = html.escape(description, quote=True).replace('\n', '<br/>')

    # Notes may be optional; if provided, escape and wrap in a div
    if notes:
        safe_notes = f'<div class="notes">{html.escape(notes, quote=True)}</div>'
    else:
        safe_notes = ''

    # Format the final HTML using the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )

    return invitation_html