import html

# Pre‑defined HTML template for the invitation.
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
    Create a secure HTML invitation string.

    Parameters
    ----------
    title_of_event : str
        The event's heading or name.
    details_of_event : str
        Full description of the event. May contain line breaks or formatting.
    when_event_is : str
        Date/time string for the event.
    extra_event_info : str
        Any user‑supplied additional notes or instructions.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering.
    """
    # Escape all user‑supplied content to prevent XSS (CWE-79).
    safe_title = html.escape(title_of_event, quote=True)
    safe_description = html.escape(details_of_event, quote=False).replace("\n", "<br>")
    safe_date = html.escape(when_event_is, quote=True)
    # For extra notes we might want to allow simple formatting (e.g., line breaks),
    # but still escape any HTML.
    safe_notes = html.escape(extra_event_info, quote=False).replace("\n", "<br>")
    # Only include the notes block if there's content.
    additional_notes_block = f"<p><strong>Additional Notes:</strong> {safe_notes}</p>" if safe_notes.strip() else ""

    # Format the invitation with sanitized content.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes=additional_notes_block
    )

    return invitation_html.strip()