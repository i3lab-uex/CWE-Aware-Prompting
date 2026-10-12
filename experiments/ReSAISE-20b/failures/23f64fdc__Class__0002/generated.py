# -*- coding: utf-8 -*-
"""
User profile rendering module.

The `generate_user_profile` function safely formats a user's name, biography
and status message into an HTML template.  All user supplied text is escaped
to prevent cross‑site scripting (XSS) and other injection attacks.
"""

import html

# Template used for rendering the profile.  The placeholders match
# the arguments of `generate_user_profile`.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="biography">{biography}</p>
    <blockquote class="status">"{status}"</blockquote>
</div>
"""

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user profile ready for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user‑written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The sanitized and formatted profile string.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    """
    # Validate input types to avoid accidental injection via non‑string objects
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be of type str")

    # Escape user input to neutralise HTML special characters.
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )