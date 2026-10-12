#!/usr/bin/env python3
"""
Secure HTML invitation builder.

This module defines a single function `build_event_invitation` that creates
an event invitation string based on a pre‑defined HTML template. All user
supplied data is properly escaped to prevent cross‑site scripting (CWE‑79).
"""

from __future__ import annotations

import html
from typing import Final


# --------------------------------------------------------------------------- #
# 1.  Pre‑defined invitation template
#
#    The placeholders are deliberately simple and unambiguous:
#      {event_title}
#      {event_description}
#      {event_date}
#      {additional_notes}
#
#    The template is intentionally minimal so that it can be safely
#    rendered in any HTML context.
# --------------------------------------------------------------------------- #
INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{event_title} – Invitation</title>
    <style>
        body {font-family: Arial, sans-serif; line-height: 1.5;}
        .header {font-size: 24px; font-weight: bold; margin-bottom: 10px;}
        .date   {font-size: 18px; color: #555; margin-bottom: 20px;}
        .content {margin-bottom: 30px;}
        .notes   {font-size: 14px; color: #777;}
    </style>
</head>
<body>
    <div class="header">{event_title}</div>
    <div class="date">Date: {event_date}</div>
    <div class="content">{event_description}</div>
    <div class="notes">{additional_notes}</div>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# 2.  Core function
#
#    The function accepts four strings, escapes them for HTML, and
#    substitutes the escaped values into `INVITATION_FORMAT`.  The escaping
#    is performed with `html.escape`, which neutralises all characters that
#    have a special meaning in HTML (`<`, `>`, `&`, `"`, `'`).  No further
#    sanitisation (e.g. stripping tags) is required because the escaping
#    guarantees that any embedded markup will be rendered literally.
#
#    Arguments:
#        title_of_event: str
#            The name or heading of the event.
#
#        details_of_event: str
#            A detailed description, possibly containing line breaks.
#
#        when_event_is: str
#            The date or time of the event.
#
#        extra_event_info: str
#            Any supplementary notes or instructions.
#
#    Returns:
#        A fully escaped HTML string that can be safely served to any
#        client without risk of XSS.
#
#    Raises:
#        TypeError: If any argument is not a string.
# --------------------------------------------------------------------------- #
def build_event_invitation(
    title_of_event: str,
    details_of_event: str,
    when_event_is: str,
    extra_event_info: str,
) -> str:
    """
    Build a secure HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The event's title.
    details_of_event : str
        Detailed description of the event.
    when_event_is : str
        Date or time of the event.
    extra_event_info : str
        Additional notes or instructions.

    Returns
    -------
    str
        Sanitised HTML representation of the invitation.
    """
    # Validate input types
    for name, value in {
        "title_of_event": title_of_event,
        "details_of_event": details_of_event,
        "when_event_is": when_event_is,
        "extra_event_info": extra_event_info,
    }.items():
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string, got {type(value).__name__}")

    # Escape all user‑supplied content
    escaped_title = html.escape(title_of_event, quote=True)
    escaped_description = html.escape(details_of_event, quote=True).replace("\n", "<br>")
    escaped_date = html.escape(when_event_is, quote=True)
    escaped_notes = html.escape(extra_event_info, quote=True).replace("\n", "<br>")

    # Format the template
    invitation_html = INVITATION_FORMAT.format(
        event_title=escaped_title,
        event_description=escaped_description,
        event_date=escaped_date,
        additional_notes=escaped_notes,
    )

    return invitation_html


# --------------------------------------------------------------------------- #
# 3.  Example usage (uncomment to test)
#
# if __name__ == "__main__":
#     print(
#         build_event_invitation(
#             title_of_event="Annual Gala",
#             details_of_event="Join us for an evening of celebration and networking.\nHighlights include a keynote address, live music, and a silent auction.",
#             when_event_is="2026-12-15 19:00",
#             extra_event_info="Dress code: Formal. Please RSVP by December 1st.",
#         )
#     )