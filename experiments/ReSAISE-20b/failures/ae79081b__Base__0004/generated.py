import html

# Predefined HTML template with placeholders for the event details.
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
    <section>{event_description}</section>
    <aside>{additional_notes}</aside>
</body>
</html>
"""

def prepare_event_details(headline: str,
                          summary: str,
                          scheduled_date: str,
                          additional_info: str) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        Title or name of the event.
    summary : str
        Comprehensive description of the event (may include multiple paragraphs).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        A string containing sanitized HTML for secure display of the event invitation.

    Raises
    ------
    ValueError
        If any required argument is not a string.
    """
    # Basic type validation to avoid accidental injection via non-string objects
    for name, value in [("headline", headline),
                        ("summary", summary),
                        ("scheduled_date", scheduled_date),
                        ("additional_info", additional_info)]:
        if not isinstance(value, str):
            raise ValueError(f"{name!r} must be a string")

    # Escape all user-supplied content to prevent XSS
    escaped_headline = html.escape(headline, quote=True)
    escaped_summary = html.escape(summary, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_info = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Format the sanitized content into the HTML template
    return INVITATION_FORMAT.format(
        event_title=escaped_headline,
        event_description=escaped_summary,
        event_date=escaped_date,
        additional_notes=escaped_info
    )