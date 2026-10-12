import html

# Predefined HTML template for the invitation.
INVITATION_FORMAT = """
<div class="invitation">
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="additional">{additional_notes}</div>
</div>
"""

def prepare_event_details(headline: str,
                          summary: str,
                          scheduled_date: str,
                          additional_info: str) -> str:
    """
    Generate a secure, sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        Title or name of the event.
    summary : str
        Comprehensive description (may contain newlines, paragraphs).
    scheduled_date : str
        Scheduled date of the event.
    additional_info : str
        Supplementary information or instructions.

    Returns
    -------
    str
        Sanitized HTML string ready for safe rendering in a browser.

    Notes
    -----
    * All user-provided content is escaped using `html.escape` to prevent XSS.
    * The function does not perform HTML validation beyond escaping; it assumes the
      surrounding environment (e.g., a template engine) will not add additional markup.
    * This approach mitigates CWE-707 by ensuring the content is well‑formed
      and neutralized before being incorporated into the output.
    """
    # Escape all user input to prevent injection attacks.
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True).replace('\n', '<br>')
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional = html.escape(additional_info, quote=True).replace('\n', '<br>')

    # Format the invitation using the predefined template.
    html_content = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional
    )

    return html_content.strip()