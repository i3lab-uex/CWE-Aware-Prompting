import html

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_of_event} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color:#f2f2f2; padding: 10px; border-radius:5px; }}
        .details {{ margin-top:20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title_of_event}</h1>
        <p><strong>Date:</strong> {scheduled_date}</p>
    </div>
    <div class="details">
        <h2>Details</h2>
        <p>{event_details}</p>
    </div>
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
    Generates a sanitized HTML invitation for an event.

    Args:
        title_of_event: Name or title of the event.
        event_details: Comprehensive description (may contain newlines).
        scheduled_date: Scheduled date for the event.
        extra_info: Additional information or instructions.

    Returns:
        A string containing sanitized HTML ready for safe display.
    """
    # Escape all user-provided content to neutralize any HTML injection
    safe_title = html.escape(title_of_event, quote=True)
    safe_details = html.escape(event_details, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_extra = html.escape(extra_info, quote=True).replace('\n', '<br>')

    # Prepare the optional extra section
    if safe_extra.strip():
        extra_section = f"""
        <div class="extra">
            <h2>Additional Notes</h2>
            <p>{safe_extra}</p>
        </div>
        """
    else:
        extra_section = ""

    # Format the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_section=extra_section
    )

    return invitation_html.strip()