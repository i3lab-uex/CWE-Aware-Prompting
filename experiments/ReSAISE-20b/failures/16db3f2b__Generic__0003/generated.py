# -*- coding: utf-8 -*-

"""
Utility module for rendering user profiles safely for web display.
"""

from html import escape
from typing import Final

# Template used to format the user profile.  The placeholders are named
# {username}, {bio} and {status_message}.  Adjust the template as needed.
PROFILE_FORMAT: Final[str] = (
    "<div class='user-profile'>"
    "  <h2>{username}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <footer class='status'>Status: {status_message}</footer>"
    "</div>"
)


def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as they entered it.
    bio : str
        A user-written biography that may span multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The profile HTML string with all user-provided data safely escaped.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    if not all(isinstance(arg, str) for arg in (username, bio, status_message)):
        raise ValueError("All arguments must be strings")

    # Escape HTML special characters to prevent XSS attacks.
    safe_username = escape(username, quote=True)
    safe_bio = escape(bio, quote=False)  # keep quotes to preserve formatting
    safe_status = escape(status_message, quote=True)

    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )