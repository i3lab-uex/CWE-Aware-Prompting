# -*- coding: utf-8 -*-
"""
User profile generation module.

This module provides a single function `generate_user_profile` that safely
constructs an HTML snippet for displaying a user profile.  All user supplied
text is escaped to prevent XSS attacks and the final string is guaranteed to be
well‑formed HTML, mitigating CWE‑707 concerns.
"""

from __future__ import annotations

import html
from typing import Final


# Example template: replace with the actual format used in your application.
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"about-me\">{bio}</p>\n"
    "  <footer><em>{status}</em></footer>\n"
    "</div>"
)


def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized HTML user profile snippet.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile ready for
        safe web display.

    Notes
    -----
    - All input strings are escaped using :func:`html.escape` to neutralise
      potentially malicious markup.
    - The function does not rely on any external templating engine, keeping
      dependencies minimal and the output deterministic.
    """
    # Escape user input to prevent XSS attacks
    safe_name = html.escape(full_name, quote=True)
    safe_bio = html.escape(about_me, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)