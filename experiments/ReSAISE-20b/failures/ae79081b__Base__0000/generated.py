import html

# Predefined HTML template with placeholders for the event invitation.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h1>{event_title}</h1>
    <div class="description">{event_description}</div>
    <p><strong>Date:</strong> {event_date}</p>
    <div class="additional-notes">{additional_notes}</div>
</div>
"""

def prepare_event_details(headline: str, summary: str,
                          scheduled_date: str, additional_info: str) -> str:
    """
    Generates a secure HTML representation of an event invitation.

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
        Sanitized HTML string suitable for safe rendering in a web page.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    """
    # Validate input types
    for name, value in {
        "headline": headline,
        "summary": summary,
        "scheduled_date": scheduled_date,
        "additional_info": additional_info
    }.items():
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string")

    # Escape user-provided content to prevent XSS
    escaped_headline = html.escape(headline, quote=True)
    escaped_summary = html.escape(summary, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(scheduled_date, quote=True)
    escaped_additional = html.escape(additional_info, quote=True).replace("\n", "<br>")

    # Format the invitation using the predefined template
    return INVITATION_FORMAT.format(
        event_title=escaped_headline,
        event_description=escaped_summary,
        event_date=escaped_date,
        additional_notes=escaped_additional
    )