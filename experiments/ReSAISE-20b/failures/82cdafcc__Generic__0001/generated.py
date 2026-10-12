# -*- coding: utf-8 -*-
"""
Utility for safely rendering a user profile on the web.

The `display_user_profile` function accepts raw strings provided by the
user and returns a fully escaped HTML snippet that can be inserted into
a template.  The implementation uses :func:`html.escape` to neutralise
any potentially malicious input, protecting against XSS attacks.
"""

import html

# Example template.  In real code this would probably live in a separate
# template file or be defined by the web framework.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <footer class="status">Status: {status}</footer>
</div>
"""

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML representation of a user profile.

    Parameters
    ----------
    person_name : str
        The name supplied by the user.
    user_bio : str
        A multi‑sentence biography written by the user.
    status_message : str
        A short status update.

    Returns
    -------
    str
        An HTML string with all user input escaped and inserted into the
        :data:`PROFILE_FORMAT` template.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checking to avoid accidental injection of non‑string objects
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise TypeError("All arguments must be of type 'str'")

    # Escape user input to prevent XSS
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)