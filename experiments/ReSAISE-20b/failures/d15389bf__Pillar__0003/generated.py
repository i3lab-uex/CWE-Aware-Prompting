import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{font-family: Arial, sans-serif; margin: 20px;}}
  .event-title {{font-size: 1.5em; font-weight: bold; margin-bottom: 10px;}}
  .event-date {{color: #555; margin-bottom: 20px;}}
  .event-description, .event-notes {{margin-bottom: 15px; white-space: pre-wrap;}}
</style>
</head>
<body>
<div class="event">
  <div class="event-title">{title}</div>
  <div class="event-date">Date: {date}</div>
  <div class="event-description">{description}</div>
  <div class="event-notes">Notes: {notes}</div>
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The name or title of the event.
    description : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date : str
        The scheduled date for the event.
    notes : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or empty.
    """
    # Basic validation: ensure all inputs are provided and non-empty
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise ValueError("All arguments must be strings.")
    if not title.strip():
        raise ValueError("Title cannot be empty.")
    if not date.strip():
        raise ValueError("Date cannot be empty.")

    # Escape user-provided content to prevent XSS and other injection attacks.
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