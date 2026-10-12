import html

# Predefined HTML template with placeholders for event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 2rem; }}
  .event-title {{ font-size: 2rem; font-weight: bold; margin-bottom: 1rem; }}
  .event-date {{ color: #555; margin-bottom: 1rem; }}
  .event-description, .event-notes {{ white-space: pre-wrap; margin-bottom: 1rem; }}
</style>
</head>
<body>
<div class="event">
    <div class="event-title">{title}</div>
    <div class="event-date">Date: {date}</div>
    <div class="event-description">{description}</div>
    <div class="event-notes">{notes}</div>
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The name or title of the event.
    description : str
        A comprehensive description of the event (may contain multiple lines).
    date : str
        The scheduled date for the event.
    notes : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.

    Raises
    ------
    ValueError
        If any of the required arguments are not strings.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise ValueError("All arguments must be strings.")

    # Escape user-provided content to prevent XSS (CWE-79)
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=True)

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )