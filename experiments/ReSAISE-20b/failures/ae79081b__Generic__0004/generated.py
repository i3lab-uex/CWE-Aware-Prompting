import bleach

# Define the allowed tags and attributes for safe rendering
ALLOWED_TAGS = [
    "b", "i", "strong", "em", "p", "br",
    "ul", "ol", "li", "a", "blockquote", "code"
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
}
# Ensure links open in a new tab and are safe
ALLOWED_PROTOCOLS = bleach.sanitizer.ALLOWED_PROTOCOLS.union({"mailto"})

# Predefined HTML template with placeholders
INVITATION_FORMAT = """
<div class="event-invitation">
  <h1>{event_title}</h1>
  <div class="event-description">{event_description}</div>
  <p><strong>Date:</strong> {event_date}</p>
  <div class="additional-notes">{additional_notes}</div>
</div>
"""

def prepare_event_details(headline: str, summary: str,
                          scheduled_date: str, additional_info: str) -> str:
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
        A string containing sanitized HTML for secure display of the event invitation.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    # Basic validation of required fields
    for name, value in [("headline", headline), ("summary", summary),
                        ("scheduled_date", scheduled_date)]:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Argument '{name}' must be a non-empty string.")

    # Sanitize each component
    safe_title = bleach.clean(headline, tags=[], attributes={}, protocols=ALLOWED_PROTOCOLS)
    safe_summary = bleach.clean(
        summary,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS
    )
    safe_date = bleach.clean(scheduled_date, tags=[], attributes={}, protocols=ALLOWED_PROTOCOLS)
    safe_additional = bleach.clean(
        additional_info,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS
    )

    # Render the template with sanitized content
    html_output = INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_additional
    )
    return html_output.strip()