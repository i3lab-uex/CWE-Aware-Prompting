import html

# Predefined HTML template with placeholders for event details.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <div class="event-description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="additional-notes">{additional_notes}</div>
</div>
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
        Comprehensive description of the event (may contain multiple paragraphs).
    scheduled_date : str
        Scheduled date of the event.
    additional_info : str
        Supplementary information or instructions.

    Returns
    -------
    str
        A string containing sanitized HTML suitable for secure display.
    """
    # Escape all user-supplied content to neutralize potential XSS payloads.
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_info = html.escape(additional_info, quote=True).replace('\n', '<br>')

    # Render the invitation using the safe values.
    html_output = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_info
    )

    return html_output