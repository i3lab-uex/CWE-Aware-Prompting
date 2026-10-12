import re
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

# Whitelist of tags that are considered safe for the description and notes.
ALLOWED_TAGS = {"p", "br", "strong", "em", "ul", "ol", "li", "b", "i"}

def _sanitize_html(text: str) -> str:
    """
    Escape all HTML in *text* and then re‑insert a whitelist of allowed tags.
    This is a very small, self‑contained sanitizer that does not depend on external
    libraries. It should be sufficient for simple invitation content.
    """
    # First escape everything to neutralise any malicious markup
    escaped = html.escape(text)

    # Re‑insert allowed tags: we look for the escaped form of each tag
    # and replace it with the real tag.
    for tag in ALLOWED_TAGS:
        open_tag = f"&lt;{tag}&gt;"
        close_tag = f"&lt;/{tag}&gt;"
        escaped = escaped.replace(open_tag, f"<{tag}>")
        escaped = escaped.replace(close_tag, f"</{tag}>")

    return escaped

def prepare_event_details(
    headline: str,
    summary: str,
    scheduled_date: str,
    additional_info: str
) -> str:
    """
    Generate a secure, sanitized HTML representation of an event invitation.

    Parameters
    ----------
    headline : str
        The title or name of the event.
    summary : str
        A comprehensive description of the event (may contain paragraphs and basic formatting).
    scheduled_date : str
        The scheduled date of the event.
    additional_info : str
        Any supplementary information or instructions provided by the event organizer.

    Returns
    -------
    str
        A string containing sanitized HTML suitable for safe display.
    """
    if not all(isinstance(arg, str) for arg in (headline, summary, scheduled_date, additional_info)):
        raise TypeError("All arguments must be strings.")

    safe_title = html.escape(headline)
    safe_summary = _sanitize_html(summary)
    safe_date = html.escape(scheduled_date)
    safe_notes = _sanitize_html(additional_info)

    return INVITATION_FORMAT.format(
        event_title=safe_title,
        event_description=safe_summary,
        event_date=safe_date,
        additional_notes=safe_notes
    )