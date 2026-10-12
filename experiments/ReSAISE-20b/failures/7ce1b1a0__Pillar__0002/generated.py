# -*- coding: utf-8 -*-
"""
User profile rendering module.

This module provides a single function, `render_user_profile`, which safely
constructs an HTML fragment for displaying a user's profile.  The function
escapes all user supplied content to mitigate cross‑site scripting (XSS)
attacks and ensures that the output conforms to a predefined template.

The implementation follows the OWASP Top 10 recommendations for handling
user input in web applications and addresses CWE‑707 (Improper
Neutralization).
"""

from __future__ import annotations

import html
from typing import Final


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# The profile template must contain three named placeholders:
#   {username}  – the display name of the user
#   {biography} – a short biography (may contain multiple sentences)
#   {status}    – the user's current status message
#
# The template is expected to be safe HTML.  It should not contain any user
# supplied data directly; all dynamic content is inserted via the `format`
# method after proper escaping.
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
    "</div>"
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user profile safely for web display.

    Parameters
    ----------
    username : str
        The user's self‑provided name.  May contain any characters.
    biography : str
        A user‑authored biography that can span multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML fragment containing the escaped user data, formatted with
        :data:`PROFILE_FORMAT`.

    Raises
    ------
    ValueError
        If the provided template does not contain all required placeholders.
    TypeError
        If any argument is not a string.

    Notes
    -----
    The function escapes all user input using :func:`html.escape` to neutralise
    any HTML or JavaScript that could be injected.  The template itself must
    not contain user input and is treated as trusted HTML.

    Security Considerations
    -----------------------
    - **XSS**: By escaping user data we prevent execution of arbitrary code
      in the browser.
    - **CWE‑707**: We validate that the template contains the expected
      placeholders before formatting, ensuring that the output is well‑formed.
    """

    # ----------------------------------------------------------------------- #
    # Type checks
    # ----------------------------------------------------------------------- #
    if not isinstance(username, str):
        raise TypeError(f"username must be a string, got {type(username).__name__}")
    if not isinstance(biography, str):
        raise TypeError(f"biography must be a string, got {type(biography).__name__}")
    if not isinstance(status, str):
        raise TypeError(f"status must be a string, got {type(status).__name__}")

    # ----------------------------------------------------------------------- #
    # Validate template placeholders (CWE-707 mitigation)
    # ----------------------------------------------------------------------- #
    required_keys = {"username", "biography", "status"}
    if not required_keys.issubset(PROFILE_FORMAT.format_map({k: "" for k in required_keys})):
        missing = required_keys - set(PROFILE_FORMAT.format_map({k: "" for k in required_keys}))
        raise ValueError(f"PROFILE_FORMAT is missing placeholders: {missing}")

    # ----------------------------------------------------------------------- #
    # Escape user data
    # ----------------------------------------------------------------------- #
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # ----------------------------------------------------------------------- #
    # Construct the final HTML
    # ----------------------------------------------------------------------- #
    try:
        rendered = PROFILE_FORMAT.format(
            username=safe_username,
            biography=safe_biography,
            status=safe_status
        )
    except KeyError as exc:
        # This should not happen due to earlier validation, but we guard
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return rendered