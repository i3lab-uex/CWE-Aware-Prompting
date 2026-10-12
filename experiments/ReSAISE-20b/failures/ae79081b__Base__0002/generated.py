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
    <div>{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div>{additional_notes}</div>
</body>
</html>
"""

def prepare_event_details(headline: str, summary: str,
                          scheduled_date: str, additional_info: str) -> str:
    """
    Generates a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        The title or name of the event.
    summary : str
        A comprehensive description of the event (may include multiple paragraphs).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        A fully escaped HTML string safe for rendering in a browser.
    """
    # Escape all user-provided content to neutralize any embedded HTML or script.
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional = html.escape(additional_info, quote=True).replace('\n', '<br>')

    return INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional
    )