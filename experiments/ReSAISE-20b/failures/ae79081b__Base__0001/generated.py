import html

# Example invitation template; in real use this would be defined elsewhere.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
</head>
<body>
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="additional">{additional_notes}</div>
</body>
</html>
"""

def prepare_event_details(headline: str, summary: str, scheduled_date: str,
                          additional_info: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        The title or name of the event.
    summary : str
        A comprehensive description of the event (may include multiple paragraphs and formatting).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.
    """
    # Escape all user-supplied content to prevent XSS
    escaped_headline = html.escape(headline, quote=True)
    escaped_summary = html.escape(summary, quote=True).replace('\n', '<br>')
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_additional = html.escape(additional_info, quote=True).replace('\n', '<br>')

    # Format the invitation using the predefined template
    html_output = INVITATION_FORMAT.format(
        event_title=escaped_headline,
        event_description=escaped_summary,
        event_date=escaped_date,
        additional_notes=escaped_additional
    )
    return html_output