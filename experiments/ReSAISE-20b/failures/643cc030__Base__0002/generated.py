import html

# Pre‑defined HTML template with placeholders for the event data.
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

def create_event_invitation(e_title: str, e_description: str,
                            e_date: str, e_notes: str) -> str:
    """
    Produce a sanitized HTML invitation for an event.

    Parameters
    ----------
    e_title : str
        The name or heading of the event.
    e_description : str
        A detailed description, possibly multiline and containing formatting.
    e_date : str
        The scheduled date of the event.
    e_notes : str
        Additional notes or instructions from the user.

    Returns
    -------
    str
        A string containing a safe, escaped HTML representation of the invitation.

    Notes
    -----
    All user‑supplied content is escaped using `html.escape` to prevent XSS
    (CWE‑79). The function assumes that the template itself is trusted and
    does not contain untrusted input.
    """
    # Escape all user inputs to neutralize any HTML/JS that could be injected.
    safe_title = html.escape(e_title, quote=True)
    safe_description = html.escape(e_description, quote=True).replace("\n", "<br>")
    safe_date = html.escape(e_date, quote=True)
    safe_notes = (
        f"<p><em>{html.escape(e_notes, quote=True)}</em></p>"
        if e_notes
        else ""
    )

    # Populate the template with the escaped values.
    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )