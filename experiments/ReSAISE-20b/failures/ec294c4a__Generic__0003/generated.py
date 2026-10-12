import html

# Predefined HTML template with placeholders for the invitation components.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} - Invitation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
        h1 {{ color: #2c3e50; }}
        .date {{ font-weight: bold; margin-top: 10px; }}
        .notes {{ margin-top: 20px; font-style: italic; color: #555; }}
    </style>
</head>
<body>
    <div class="invitation">
        <h1>{event_title}</h1>
        <p class="description">{event_description}</p>
        <p class="date">Date: {event_date}</p>
        <div class="notes">{additional_notes}</div>
    </div>
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
    Create a secure, sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description, may contain line breaks and formatting.
    when_event_is : str
        The date of the event.
    extra_event_info : str
        Any additional instructions or notes.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering.
    """
    # Escape all user-provided content to prevent XSS attacks.
    safe_title = html.escape(title_of_event, quote=True)
    # Preserve line breaks by converting them to <br> tags after escaping.
    safe_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Format the invitation using the predefined template.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )
    return invitation_html