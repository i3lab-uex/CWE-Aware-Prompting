# -*- coding: utf-8 -*-

"""
User profile rendering module.

This module provides a single function `generate_user_profile` that safely
renders user supplied data into an HTML snippet for web display.  All
user-supplied strings are escaped to prevent XSS attacks.
"""

import html

# Template for the user profile.  The placeholders are named
# `username`, `biography` and `status`.  This can be replaced with a
# more complex template engine if needed.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{username}</h2>
    <p class="bio">{biography}</p>
    <div class="status"><strong>Status:</strong> {status}</div>
</div>
"""


def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user‑written biography that may contain multiple sentences.
    status : str
        The user's current status message.

    Returns
    -------
    str
        An HTML snippet with the sanitized user profile information.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise ValueError("All arguments must be strings")

    # Escape user-provided content to avoid XSS
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )