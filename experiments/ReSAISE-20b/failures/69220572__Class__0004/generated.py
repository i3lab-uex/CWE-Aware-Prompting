import html
from string import Template

# Predefined HTML template with placeholders.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$title_of_event Invitation</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 20px;}
        .header {font-size: 1.5em; font-weight: bold;}
        .details, .extra {margin-top: 15px;}
    </style>
</head>
<body>
    <div class="header">$title_of_event</div>
    <div class="details">
        $event_details
    </div>
    <div class="date"><strong>Date:</strong> $scheduled_date</div>
    <div class="extra">
        $extra_info
    </div>
</body>
</html>
"""

def create_event_invitation(title_of_event: str,
                            event_details: str,
                            scheduled_date: str,
                            extra_info: str) -> str:
    """
    Generates a sanitized HTML invitation.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description (may contain newlines).
    scheduled_date : str
        The date of the event.
    extra_info : str
        Additional instructions or notes.

    Returns
    -------
    str
        A string containing the sanitized HTML invitation.
    """
    # Escape all user-provided input to neutralize special characters.
    safe_title = html.escape(title_of_event, quote=True)
    safe_details = html.escape(event_details, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_extra = html.escape(extra_info, quote=True).replace('\n', '<br>')

    template = Template(INVITATION_FORMAT)
    return template.substitute(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )