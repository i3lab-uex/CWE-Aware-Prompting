import html

# Pre‑defined HTML template with placeholders for event data.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_title}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    h1 {{ color: #333; }}
    .details, .notes {{ margin-top: 1rem; }}
</style>
</head>
<body>
<h1>{event_title}</h1>
<div class="details">{event_description}</div>
<p><strong>Date:</strong> {event_date}</p>
<div class="notes">{additional_notes}</div>
</body>
</html>
"""

def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str
) -> str:
    """
    Construct a secure, sanitized HTML invitation.

    All user supplied strings are escaped to prevent injection attacks
    (CWE‑74). The resulting HTML is safe for rendering in browsers.

    Args:
        title_of_event: Name or heading of the event.
        details_of_event: Extensive description (may contain newlines).
        when_event_is: Date of the event.
        extra_event_info: Any additional notes or instructions.

    Returns:
        A fully formed HTML string with user input safely escaped.
    """
    # Escape all inputs to neutralize special characters
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace('\n', '<br>')
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace('\n', '<br>')

    # Format the template with escaped values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html