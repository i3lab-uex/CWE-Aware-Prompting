import html

# Example invitation format template
INVITATION_FORMAT = """
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="notes">{additional_notes}</div>
</div>
"""

def prepare_event_details(
    headline: str,
    summary: str,
    scheduled_date: str,
    additional_info: str
) -> str:
    """
    Generate a sanitized HTML invitation string.

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
        A sanitized HTML string ready for safe rendering.
    """
    # Escape all user-provided content to neutralize special characters
    escaped_headline = html.escape(headline, quote=True)
    escaped_summary = html.escape(summary, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_info = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Build the final HTML using a safe template
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_headline,
        event_description=escaped_summary,
        event_date=escaped_date,
        additional_notes=escaped_info
    )
    return invitation_html