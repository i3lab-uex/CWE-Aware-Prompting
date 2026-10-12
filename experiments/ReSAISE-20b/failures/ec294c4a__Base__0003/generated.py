import html

# Predefined HTML template with placeholders for event details.
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
    <footer><em>{additional_notes}</em></footer>
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
    Build a secure, sanitized HTML representation of an event invitation.

    Parameters
    ----------
    title_of_event : str
        The name or heading of the event.
    details_of_event : str
        A detailed description of the event (may contain line breaks).
    when_event_is : str
        The date on which the event is scheduled.
    extra_event_info : str
        Any additional information or instructions provided by the user.

    Returns
    -------
    str
        A sanitized HTML string ready for safe rendering in a web page.

    Notes
    -----
    All user-provided content is escaped using html.escape to mitigate XSS (CWE-79).
    """
    # Escape all user inputs. Preserve newlines in the description by converting
    # them to <br> tags after escaping.
    safe_title = html.escape(title_of_event, quote=True)
    safe_description_raw = html.escape(details_of_event, quote=True)
    safe_date = html.escape(when_event_is, quote=True)
    safe_notes = html.escape(extra_event_info, quote=True)

    # Convert newlines in the description to <br> tags for proper HTML formatting.
    safe_description = safe_description_raw.replace("\n", "<br>\n")

    # Format the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_notes
    )

    return invitation_html