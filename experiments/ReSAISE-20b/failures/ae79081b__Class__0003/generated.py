import html

# Example invitation template with placeholders.
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
    Generate a sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        The title or name of the event.
    summary : str
        A comprehensive description of the event (may include multiple paragraphs).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the organizer.

    Returns
    -------
    str
        A string containing sanitized HTML for secure display of the event invitation.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    for arg_name, arg_value in {
        "headline": headline,
        "summary": summary,
        "scheduled_date": scheduled_date,
        "additional_info": additional_info
    }.items():
        if not isinstance(arg_value, str):
            raise TypeError(f"{arg_name} must be a string")

    # Escape all user-provided content to neutralize any HTML or script injection.
    safe_headline = html.escape(headline, quote=True)
    safe_summary = html.escape(summary, quote=True)
    safe_date = html.escape(scheduled_date, quote=True)
    safe_additional = html.escape(additional_info, quote=True)

    # Construct the final HTML by inserting the sanitized values.
    invitation_html = INVITATION_FORMAT.format(
        event_title=safe_headline,
        event_description=safe_summary.replace("\n", "<br>"),
        event_date=safe_date,
        additional_notes=safe_additional.replace("\n", "<br>")
    )

    return invitation_html