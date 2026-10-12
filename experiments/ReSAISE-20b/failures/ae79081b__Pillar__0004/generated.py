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
        Sanitized HTML string containing the event invitation.
    """
    # Ensure all inputs are strings to avoid unexpected types.
    headline = str(headline) if headline is not None else ""
    summary = str(summary) if summary is not None else ""
    scheduled_date = str(scheduled_date) if scheduled_date is not None else ""
    additional_info = str(additional_info) if additional_info is not None else ""

    # Escape HTML special characters to prevent XSS and maintain well‑formedness.
    safe_headline = html.escape(headline, quote=True)
    # For the summary and additional_info we allow line breaks but still escape.
    safe_summary = html.escape(summary, quote=True).replace("\n", "<br>")
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional_info = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Populate the template with sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional_info
    )

    return invitation_html.strip()