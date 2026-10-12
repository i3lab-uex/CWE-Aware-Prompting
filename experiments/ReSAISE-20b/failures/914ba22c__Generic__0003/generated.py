import html
from typing import Optional

# A minimal HTML template for the invitation.  The placeholders are replaced by
# the sanitized values passed to generate_event_invite().
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body style="font-family:Arial, sans-serif; line-height:1.5;">
    <h1>{event_title}</h1>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{event_description}</div>
    {additional_notes_block}
</body>
</html>
"""

def _escape_html(text: Optional[str]) -> str:
    """
    Escape special HTML characters to prevent XSS attacks.
    If the input is None, return an empty string.
    """
    if text is None:
        return ""
    # html.escape handles &, <, >, " and '.
    return html.escape(text, quote=True)

def generate_event_invite(
    title: str,
    description: str,
    date: str,
    notes: Optional[str] = None
) -> str:
    """
    Generate a secure HTML invitation for an event.

    Parameters
    ----------
    title : str
        Title or name of the event.
    description : str
        Comprehensive description, possibly containing multiple paragraphs and formatting.
    date : str
        Scheduled date of the event.
    notes : Optional[str]
        Supplementary information or instructions from the organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Sanitize all user supplied content
    safe_title = _escape_html(title)
    safe_description = _escape_html(description).replace("\n", "<br>")
    safe_date = _escape_html(date)
    safe_notes = _escape_html(notes) if notes else ""

    # Optional notes block: only included if notes were supplied
    additional_notes_block = (
        f"<div><strong>Additional Notes:</strong> {safe_notes}</div>"
        if safe_notes
        else ""
    )

    # Render the final HTML using the template
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_date=safe_date,
        event_description=safe_description,
        additional_notes_block=additional_notes_block
    )