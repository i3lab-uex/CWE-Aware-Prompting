import html

# Pre‑defined HTML template with placeholders
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    {additional_notes}
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
    Build a secure HTML representation of an event invitation.

    Args:
        title_of_event: The name or heading of the event.
        details_of_event: A comprehensive description (may contain line breaks).
        when_event_is: The date of the event.
        extra_event_info: Additional instructions or notes.

    Returns:
        A sanitized HTML string ready for safe rendering.

    Raises:
        ValueError: If any required argument is empty or None.
    """
    # Basic validation
    for name, value in [
        ("title_of_event", title_of_event),
        ("details_of_event", details_of_event),
        ("when_event_is", when_event_is)
    ]:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non‑empty string")

    # Sanitize each component
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = (
        "<br>".join(html.escape(line, quote=True) for line in details_of_event.splitlines())
    )
    safe_date = html.escape(when_event_is, quote=True)
    if extra_event_info:
        safe_notes = (
            "<p><em>Additional Notes:</em></p>"
            f"<div>{'<br>'.join(html.escape(line, quote=True) for line in extra_event_info.splitlines())}</div>"
        )
    else:
        safe_notes = ""

    # Format the final HTML
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )

    return invitation_html