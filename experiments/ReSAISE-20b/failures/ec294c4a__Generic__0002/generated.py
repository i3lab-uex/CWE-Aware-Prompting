import html

# Pre‑defined HTML template for the invitation.
# The placeholders will be replaced with escaped values.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <hr>
    <div>{event_description}</div>
    <hr>
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
    Build a secure HTML invitation from user supplied data.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description of the event. May contain line breaks or formatting.
    when_event_is : str
        The date of the event.
    extra_event_info : str
        Any additional instructions or notes from the user.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering.
    """
    # Escape all user supplied data to prevent XSS or HTML injection
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    # For extra info we allow line breaks but still escape the content
    safe_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Insert the escaped values into the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=safe_notes
    )

    return invitation_html