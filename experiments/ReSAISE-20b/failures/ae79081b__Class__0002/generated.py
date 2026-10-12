import html

# Predefined HTML template with placeholders for the invitation details.
INVITATION_FORMAT = """
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="additional-notes">{additional_notes}</div>
</div>
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
        The title or name of the event.
    summary : str
        A comprehensive description of the event. May contain multiple paragraphs and formatting.
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        Sanitized HTML string suitable for safe rendering in a browser.

    Notes
    -----
    All user-provided content is escaped using `html.escape` to mitigate CWE-74
    (Improper Neutralization of Special Elements in Output Used by a Downstream Component).
    This ensures that any HTML or script tags embedded in the input are treated as
    literal text rather than executable code.
    """
    # Escape all user-supplied content to neutralize special characters
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True)
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional_info = html.escape(additional_info, quote=True)

    # Populate the template with sanitized values
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional_info
    )

    return invitation_html.strip()