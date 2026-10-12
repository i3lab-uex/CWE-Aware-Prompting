import html

# Pre‑defined HTML template with placeholders for the invitation fields.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .invitation {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
        .header {{ font-size: 24px; margin-bottom: 10px; }}
        .date {{ color: #555; margin-bottom: 20px; }}
        .notes {{ font-style: italic; color: #333; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="invitation">
        <div class="header">{event_title}</div>
        <div class="date">Date: {event_date}</div>
        <div class="description">{event_description}</div>
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
    Build a secure HTML invitation for an event.

    All user supplied text is escaped to prevent XSS and other injection attacks.
    The resulting HTML uses a fixed template, ensuring that only the intended
    placeholders are replaced and no arbitrary tags can be injected.

    Args:
        title_of_event: The event's name or heading.
        details_of_event: A detailed description (may contain line breaks).
        when_event_is: The scheduled date of the event.
        extra_event_info: Any additional notes or instructions.

    Returns:
        A sanitized HTML string ready for rendering.
    """
    # Escape all user input to neutralize malicious content
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Format the invitation with the sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html