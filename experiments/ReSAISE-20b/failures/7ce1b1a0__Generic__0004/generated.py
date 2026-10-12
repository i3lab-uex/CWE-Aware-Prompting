# -*- coding: utf-8 -*-

"""
Utility module for rendering user profiles in a web interface.
"""

import html
from typing import Final

# Predefined template for the user profile.  The placeholders are expected to be
# named 'username', 'biography' and 'status'.
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)


def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized HTML snippet that displays a user's profile.

    Parameters
    ----------
    username : str
        The user's self-provided name.
    biography : str
        A user-authored biography that may contain multiple sentences and
        arbitrary text.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile ready for
        safe web display.

    Notes
    -----
    * All user-supplied content is escaped using :func:`html.escape` to
      prevent cross‑site scripting (XSS) attacks.
    * The function does not perform any additional validation on the
      length or content of the arguments; callers should enforce any domain‑specific
      constraints before calling this helper.
    """
    # Sanitize each user input to avoid injection of malicious HTML/JS
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )