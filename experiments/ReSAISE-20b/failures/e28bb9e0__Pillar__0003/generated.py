import html
from string import Template

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$event_title - Invitation</title>
    <style>
        body {font-family: Arial, sans-serif; line-height: 1.6;}
        .invitation {max-width: 600px; margin: auto; padding: 20px; border:1px solid #ddd;}
        .header {font-size: 24px; margin-bottom: 10px;}
        .date {color: #555; font-size: 18px; margin-bottom: 20px;}
        .notes {font-style: italic; color:#333; margin-top: 20px;}
    </style>
</head>
<body>
<div class="invitation">
    <div class="header">$event_title</div>
    <div class="date">Date: $event_date</div>
    <div class="description">$event_description</div>
    <div class="notes">Additional Notes: $additional_notes</div>
</div>
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event. May contain multiple paragraphs and formatting.
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe rendering in a browser.

    Raises
    ------
    ValueError
        If any of the required parameters are empty or not strings.
    """
    # Basic type and emptiness checks
    for arg_name, arg_val in [("title", title), ("description", description),
                              ("date", date), ("notes", notes)]:
        if not isinstance(arg_val, str):
            raise ValueError(f"Argument '{arg_name}' must be a string.")
        if not arg_val.strip():
            raise ValueError(f"Argument '{arg_name}' cannot be empty or whitespace.")

    # Escape user-provided content to neutralize XSS
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=False).replace("\n", "<br>")
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Render the template
    tmpl = Template(INVITATION_FORMAT)
    sanitized_html = tmpl.substitute(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes
    )
    return sanitized_html