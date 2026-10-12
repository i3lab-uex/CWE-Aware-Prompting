import html

# Predefined HTML template with placeholders for title, description, date, and notes.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
  .invitation {{ border: 1px solid #ccc; padding: 20px; margin: 20px auto; max-width: 600px; }}
  h1 {{ color: #2c3e50; }}
  .details {{ margin-top: 10px; }}
</style>
</head>
<body>
<div class="invitation">
  <h1>{title}</h1>
  <div class="details"><strong>Date:</strong> {date}</div>
  <p>{description}</p>
  <footer class="notes">{notes}</footer>
</div>
</body>
</html>
"""

def generate_event_invite(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

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
        A string containing sanitized HTML for safely displaying the event invitation.
    """
    # Escape all user-provided content to prevent XSS and ensure well‑formed HTML.
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=False).replace("\n", "<br>")
    safe_date = html.escape(date, quote=True)
    safe_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Fill the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        title=safe_title,
        description=safe_description,
        date=safe_date,
        notes=safe_notes
    )

    return invitation_html