import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
  .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
  .header {{ font-size: 24px; margin-bottom: 10px; }}
  .date {{ color: #555; margin-bottom: 20px; }}
  .description, .notes {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<div class="invitation">
  <div class="header">{title}</div>
  <div class="date">Date: {date}</div>
  <div class="description">{description}</div>
  <hr/>
  <div class="notes">{notes}</div>
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
        Sanitized HTML string containing the event invitation.

    Notes
    -----
    All user-provided content is escaped using `html.escape` to prevent XSS attacks.
    The template itself is static and trusted, so no further sanitization of the
    template string is required.
    """
    # Escape all user-supplied content to neutralize malicious input.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False)
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False)

    # Populate the template with sanitized values.
    return INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )