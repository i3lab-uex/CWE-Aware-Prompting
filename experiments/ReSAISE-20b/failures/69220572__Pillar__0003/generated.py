# -*- coding: utf-8 -*-
"""
Secure event invitation generator.

This module defines a single public function, `create_event_invitation`, which
produces an HTML snippet that can be safely embedded in a web page.  All user‑supplied
text is escaped to prevent cross‑site scripting (XSS) attacks, and newline characters
are converted to <br> tags so that multi‑line descriptions are preserved.

The implementation follows best practices for sanitizing user input and
avoids the CWE‑707 vulnerability by ensuring that all data inserted into the
template is well‑formed and does not contain executable content.
"""

import html

# Predefined HTML template with placeholders.  The placeholder names are
# intentionally simple and match the function argument names.
INVITATION_FORMAT = """
<div class="event-invitation">
    <h2>{title_of_event}</h2>
    <p class="details">{event_details}</p>
    <p class="date"><strong>Date:</strong> {scheduled_date}</p>
    <div class="extra-info">{extra_info}</div>
</div>
"""

def _sanitize(text: str) -> str:
    """
    Escape all HTML special characters in *text* to neutralise any
    potentially malicious content.  Newlines are converted to <br> tags
    so that multi‑line strings are displayed correctly.

    Args:
        text: Raw user input string.

    Returns:
        A safe, HTML‑escaped string with preserved line breaks.
    """
    # First escape the text to neutralise HTML special characters
    escaped = html.escape(text, quote=True)
    # Convert newlines to <br> for formatting
    return escaped.replace("\n", "<br>")

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a secure HTML representation of an event invitation.

    All inputs are sanitized to prevent XSS attacks.  The function uses a
    predefined template, `INVITATION_FORMAT`, and substitutes the
    placeholders with sanitized values.

    Args:
        title_of_event: The name or title of the event.
        event_details: A comprehensive description of the event
                       (may contain multiple lines and formatting).
        scheduled_date: The scheduled date for the event.
        extra_info: Extra information or instructions provided by the user.

    Returns:
        A string containing sanitized HTML ready for safe display.
    """
    # Sanitize all inputs
    safe_title = _sanitize(title_of_event)
    safe_details = _sanitize(event_details)
    safe_date = _sanitize(scheduled_date)
    safe_extra = _sanitize(extra_info)

    # Populate the template
    return INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )