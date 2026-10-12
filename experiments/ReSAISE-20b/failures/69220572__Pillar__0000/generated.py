import html
from typing import Final

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title_of_event}</title>
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.5; }}
  .invitation {{ border: 1px solid #ccc; padding: 20px; max-width: 600px; margin: auto; }}
  .header {{ font-size: 1.5em; margin-bottom: 10px; }}
  .details {{ white-space: pre-wrap; }}
  .footer {{ margin-top: 20px; font-size: 0.9em; color:#555; }}
</style>
</head>
<body>
<div class="invitation">
  <div class="header">{title_of_event}</div>
  <div class="details">{event_details}</div>
  <div class="footer">
    <strong>Date:</strong> {scheduled_date}<br>
    <em>{extra_info}</em>
  </div>
</div>
</body>
</html>
"""

def _sanitize_html(text: str) -> str:
    """
    Escapes HTML special characters to prevent injection.
    Preserves line breaks by converting them to <br> tags after escaping.
    """
    # Escape first
    escaped = html.escape(text)
    # Replace newline characters with <br> tags for display
    return escaped.replace("\n", "<br>\n")

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a secure, sanitized HTML invitation string.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event (may contain multiple lines).
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the invitation.
    """
    # Sanitize each component to neutralize potential script injections
    safe_title = _sanitize_html(title_of_event)
    safe_details = _sanitize_html(event_details)
    safe_date = _sanitize_html(scheduled_date)
    safe_extra = _sanitize_html(extra_info)

    # Populate the template with sanitized data
    return INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )