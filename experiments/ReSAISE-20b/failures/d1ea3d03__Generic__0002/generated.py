# -*- coding: utf-8 -*-
"""
Utility for rendering a user profile page with basic HTML escaping
to prevent XSS vulnerabilities.
"""

from html import escape

# Example template: placeholders are named for clarity
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted profile information.

    Raises
    ------
    TypeError
        If any of the arguments are not strings.
    """
    if not isinstance(fullname, str):
        raise TypeError(f"fullname must be a string, got {type(fullname).__name__}")
    if not isinstance(biography, str):
        raise TypeError(f"biography must be a string, got {type(biography).__name__}")
    if not isinstance(status_message, str):
        raise TypeError(f"status_message must be a string, got {type(status_message).__name__}")

    # Escape user-provided content to avoid XSS
    safe_name = escape(fullname, quote=True)
    safe_bio = escape(biography, quote=True)
    safe_status = escape(status_message, quote=True)

    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)