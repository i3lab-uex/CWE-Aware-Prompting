import html

# Predefined HTML template with placeholders for the invitation details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{event_name} Invitation</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
    .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
    h1 {{ color: #333; }}
    .date {{ font-weight: bold; margin-top: 10px; }}
    .notes {{ background:#f9f9f9; padding:10px; margin-top:15px; border-left:4px solid #007BFF; }}
</style>
</head>
<body>
<div class="container">
    <h1>{event_name}</h1>
    <div class="description">{description_of_event}</div>
    <div class="date">Date: {date_of_event}</div>
    <div class="notes">{notes_for_event}</div>
</div>
</body>
</html>
"""

def create_invitation_for_event(
    event_name: str,
    description_of_event: str,
    date_of_event: str,
    notes_for_event: str
) -> str:
    """
    Generates a sanitized HTML invitation for an event.

    Parameters
    ----------
    event_name : str
        The name or title of the event.
    description_of_event : str
        A comprehensive description of the event (may contain multiple lines and formatting).
    date_of_event : str
        The scheduled date for the event.
    notes_for_event : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A string containing sanitized HTML for safely displaying the event invitation.

    Notes
    -----
    All user-supplied content is escaped using `html.escape` to prevent XSS attacks.
    The function does not allow arbitrary HTML injection; only plain text is rendered
    with the styling defined in `INVITATION_FORMAT`.
    """
    # Escape user-provided strings to avoid injection attacks
    safe_event_name = html.escape(event_name, quote=True)
    safe_description = html.escape(description_of_event, quote=True).replace("\n", "<br>")
    safe_date = html.escape(date_of_event, quote=True)
    safe_notes = html.escape(notes_for_event, quote=True).replace("\n", "<br>")

    # Format the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_name=safe_event_name,
        description_of_event=safe_description,
        date_of_event=safe_date,
        notes_for_event=safe_notes
    )

    return invitation_html