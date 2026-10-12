import html

# Predefined HTML template with placeholders for event data.
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
    {additional_notes_block}
</body>
</html>
"""

def create_event_invitation(title: str, description: str, date: str, notes: str) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title : str
        The title or name of the event.
    description : str
        A comprehensive description of the event. May contain multiple paragraphs and formatting.
    date : str
        The scheduled date of the event.
    notes : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        A string containing sanitized HTML for secure display of the event invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types to avoid accidental injection via non-string objects
    if not all(isinstance(arg, str) for arg in (title, description, date, notes)):
        raise TypeError("All arguments must be of type 'str'")

    # Escape all user-provided content to neutralize special characters
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=False).replace("\n", "<br>")
    escaped_date = html.escape(date, quote=True)
    escaped_notes = html.escape(notes, quote=False).replace("\n", "<br>")

    # Prepare the notes block only if notes are provided
    additional_notes_block = (
        f"<div><strong>Additional Notes:</strong>{escaped_notes}</div>"
        if notes.strip()
        else ""
    )

    # Populate the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes_block=additional_notes_block
    )

    return invitation_html.strip()