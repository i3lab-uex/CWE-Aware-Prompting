import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
    .invitation {{ border: 1px solid #ccc; padding: 20px; margin: 20px auto; max-width: 600px; }}
    h1 {{ color: #333; }}
    .notes {{ margin-top: 20px; font-style: italic; color: #555; }}
</style>
</head>
<body>
<div class="invitation">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    <div class="notes">{additional_notes}</div>
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event (may include multiple paragraphs and formatting).
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe rendering in a web page.

    Raises
    ------
    ValueError
        If any of the required arguments are empty or not strings.
    """
    # Basic validation
    for arg_name, value in (("title", title), ("description", description),
                            ("date", date), ("notes", notes)):
        if not isinstance(value, str):
            raise ValueError(f"{arg_name} must be a string")
        if not value.strip():
            raise ValueError(f"{arg_name} cannot be empty")

    # Escape all user-provided content to prevent injection attacks.
    safe_title = html.escape(title, quote=True)
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