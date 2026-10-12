#!/usr/bin/env python3
"""
Secure event invitation generator.

This module provides a single function, `create_event_invitation`, which
produces an HTML string that can safely be embedded in a web page. All user‑supplied
text is escaped to prevent cross‑site scripting (XSS) and other injection attacks.
"""

from __future__ import annotations

import html
import re
from typing import Final


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

INVITATION_FORMAT: Final[str] = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title_of_event}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    h1 {{ color: #333; }}
    .details, .extra {{ margin-top: 1rem; white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>{title_of_event}</h1>
<div class="details">{event_details}</div>
<p><strong>Date:</strong> {scheduled_date}</p>
<div class="extra">{extra_info}</div>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _sanitize_html(raw: str) -> str:
    """
    Escape all HTML special characters in the input string.
    Additionally, remove any <script> tags that might have been inserted
    after escaping (to guard against malformed input that tries to break out).
    """
    # Escape HTML
    escaped = html.escape(raw, quote=True)

    # Remove any <script>...</script> patterns (case‑insensitive)
    script_pattern = re.compile(r"<\s*script[^>]*>(.*?)<\s*/\s*script\s*>",
                                flags=re.IGNORECASE | re.DOTALL)
    cleaned = script_pattern.sub("", escaped)

    return cleaned


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def create_event_invitation(
    title_of_event: str,
    event_details: str,
    scheduled_date: str,
    extra_info: str
) -> str:
    """
    Generate a sanitized HTML invitation for an event.

    Parameters
    ----------
    title_of_event : str
        The name or title of the event.
    event_details : str
        A comprehensive description of the event. May contain newlines and formatting.
    scheduled_date : str
        The scheduled date for the event.
    extra_info : str
        Extra information or instructions provided by the user.

    Returns
    -------
    str
        A complete, sanitized HTML document ready for display.
    """
    # Sanitize each component
    safe_title = _sanitize_html(title_of_event)
    safe_details = _sanitize_html(event_details)
    safe_date = _sanitize_html(scheduled_date)
    safe_extra = _sanitize_html(extra_info)

    # Format the template
    invitation_html = INVITATION_FORMAT.format(
        title_of_event=safe_title,
        event_details=safe_details,
        scheduled_date=safe_date,
        extra_info=safe_extra
    )

    return invitation_html


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    example_html = create_event_invitation(
        title_of_event="Annual Gala",
        event_details=(
            "Join us for an evening of celebration, "
            "fine dining, and live music.\n\n"
            "Dress code: Formal attire."
        ),
        scheduled_date="2026-08-15",
        extra_info=(
            "RSVP by July 31st.\n"
            "For inquiries, contact <script>alert('xss');</script>"
        )
    )
    print(example_html)