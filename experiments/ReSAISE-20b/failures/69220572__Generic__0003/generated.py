import html

# Predefined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title_of_event}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; }}
  .event-title {{ font-size: 2em; font-weight: bold; margin-bottom: 10px; }}
  .event-details {{ white-space: pre-wrap; margin-bottom: 15px; }}
  .event-date {{ font-weight: bold; margin-bottom: 10px; }}
  .extra-info {{ color: #555; }}
</style>
</head>
<body>
<div class="event-title">{title_of_event}</div>
<div class="event-date">Date: {scheduled_date}</div>
<div class="event-details">{event_details}</div>
{extra_section}
</body>
</html>
"""

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event. May contain newlines and formatting.
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        Sanitized HTML string ready for safe rendering.
    """
    # Escape all user-provided content to prevent XSS attacks.
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_details = html.escape(event_details, quote=True)
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_extra = html.escape(extra_info, quote=True)

    # Include the extra section only if there's content.
    if escaped_extra.strip():
        extra_section = f'<div class="extra-info">Additional Notes: {escaped_extra}</div>'
    else:
        extra_section = ''

    # Format the final HTML with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=escaped_title,
        event_details=escaped_details,
        scheduled_date=escaped_date,
        extra_section=extra_section
    )

    return invitation_html