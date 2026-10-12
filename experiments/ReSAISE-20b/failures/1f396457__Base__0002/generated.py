import html

# Pre‑defined template for the invitation.  It contains placeholders that will be
# replaced with sanitized values.
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
{additional_notes_section}
</body>
</html>
"""

def _escape_html(text: str) -> str:
    """
    Escape special HTML characters in a string to prevent XSS.
    """
    return html.escape(text, quote=True)

def generate_event_html(title: str,
                        description: str,
                        date: str,
                        extra_notes: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    title : str
        The name or heading of the event.
    description : str
        A detailed description of the event. May contain line breaks or Markdown‑style
        formatting, but all characters are escaped before rendering.
    date : str
        The scheduled date of the event. Treated as plain text and escaped.
    extra_notes : str
        Any additional instructions or information supplied by the user. Escaped.

    Returns
    -------
    str
        A sanitized HTML string that can be safely served to users.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (title, description, date, extra_notes)):
        raise TypeError("All arguments must be of type 'str'")

    # Escape all user inputs to neutralize potential XSS payloads
    safe_title = _escape_html(title)
    safe_description = _escape_html(description).replace("\n", "<br>")
    safe_date = _escape_html(date)
    safe_notes = _escape_html(extra_notes)

    # Only include the notes section if there is content
    notes_section = (
        f"<div><strong>Additional Notes:</strong>{safe_notes}</div>"
        if safe_notes.strip()
        else ""
    )

    # Render the template with sanitized values
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes_section=notes_section
    )