import html

# Predefined HTML template for the invitation. 
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

def prepare_event_details(headline: str,
                          summary: str,
                          scheduled_date: str,
                          additional_info: str) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        Title or name of the event.
    summary : str
        Comprehensive description (may contain multiple paragraphs).
    scheduled_date : str
        Scheduled date of the event.
    additional_info : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML ready for safe rendering.
    """
    # Sanitize each component to prevent XSS and other injection attacks
    safe_title = html.escape(headline, quote=True)
    # Preserve paragraph breaks by converting newlines to <br> after escaping
    safe_description = html.escape(summary, quote=True).replace("\n", "<br>")
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Populate the template safely
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_description,
        event_date=safe_date,
        additional_notes=safe_additional
    )

    return invitation_html