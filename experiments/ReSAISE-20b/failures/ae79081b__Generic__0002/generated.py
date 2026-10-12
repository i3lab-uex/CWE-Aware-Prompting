import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .event-title {{ font-size: 2em; margin-bottom: 0.5em; }}
        .event-date {{ color: #555; font-size: 1.2em; margin-bottom: 1em; }}
        .event-description {{ margin-bottom: 1.5em; }}
        .additional-notes {{ font-style: italic; color: #333; }}
    </style>
</head>
<body>
    <div class="event-title">{event_title}</div>
    <div class="event-date">Date: {event_date}</div>
    <div class="event-description">{event_description}</div>
    <div class="additional-notes">{additional_notes}</div>
</body>
</html>
"""

def prepare_event_details(
    headline: str,
    summary: str,
    scheduled_date: str,
    additional_info: str
) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        Title or name of the event.
    summary : str
        Comprehensive description of the event (may include multiple paragraphs).
    scheduled_date : str
        Scheduled date of the event.
    additional_info : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe display.

    Notes
    -----
    The function uses `html.escape` to neutralize any HTML or script content in the
    input parameters, preventing XSS attacks. The returned string is safe to embed
    in a web page without further escaping.
    """
    # Escape all user-supplied content
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True).replace("\n", "<br>")
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional_info = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Format the template with sanitized values
    html_content = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_date=safe_date,
        event_description=safe_summary,
        additional_notes=safe_additional_info
    )

    return html_content