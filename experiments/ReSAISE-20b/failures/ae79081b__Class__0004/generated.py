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

def prepare_event_details(headline: str, summary: str, scheduled_date: str, additional_info: str) -> str:
    """
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        The title or name of the event.
    summary : str
        A comprehensive description of the event (may contain multiple paragraphs and formatting).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        A string containing sanitized HTML ready for secure display.
    """
    # Escape all user-supplied content to prevent XSS and injection attacks
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True)
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional = html.escape(additional_info, quote=True)

    # Build the final HTML using the safe values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional
    )

    return invitation_html.strip()