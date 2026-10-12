# -*- coding: utf-8 -*-
"""
User profile rendering module.

This module provides a single function `render_user_profile` that takes
user‑supplied data, sanitises it to prevent XSS and other injection attacks,
and injects the cleaned values into a pre‑defined template.

Security notes
--------------
* All user inputs are passed through `html.escape` which neutralises any
  HTML or JavaScript that could be executed in a browser context.
* The template is treated as read‑only; placeholders are replaced by the
  sanitized values only.
* No external data is parsed or executed, mitigating CWE‑707 risks.
"""

from __future__ import annotations

import html
from typing import Final


# Example template – in a real application this would be loaded from a file
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <div class=\"status\"><strong>Status:</strong> {status}</div>\n"
    "</div>"
)


def _sanitize(value: str) -> str:
    """
    Escape a string for safe inclusion in HTML.

    Parameters
    ----------
    value : str
        The raw user input.

    Returns
    -------
    str
        A version of the string safe for HTML rendering.
    """
    # html.escape replaces &, <, >, " and '
    return html.escape(value, quote=True)


def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized user profile HTML snippet.

    Parameters
    ----------
    username : str
        The user's self‑provided name.
    biography : str
        A user‑authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted profile ready for web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checking – helps prevent accidental injection of non‑string
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be of type str")

    # Sanitize each component
    safe_username = _sanitize(username)
    safe_biography = _sanitize(biography)
    safe_status = _sanitize(status)

    # Render the final template
    rendered_profile = PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )

    return rendered_profile


# Example usage (for manual testing only)
if __name__ == "__main__":
    sample = render_user_profile(
        "Alice <script>alert('xss')</script>",
        "I love coding. <b>Python</b> is my favorite.",
        "Working on a new project!"
    )
    print(sample)