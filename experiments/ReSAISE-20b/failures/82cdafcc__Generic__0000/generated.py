# -*- coding: utf-8 -*-

"""
Utility to safely render a user profile for a web interface.
"""

import html
from typing import Any

# Example template; in real usage this would be defined elsewhere.
PROFILE_FORMAT: str = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)


def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML snippet representing the user's profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A user‑authored biography that may contain multiple sentences.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string with all user data escaped and inserted into the
        PROFILE_FORMAT template.

    Raises
    ------
    ValueError
        If any of the required arguments is empty or not a string.
    """
    # Basic type and emptiness checks
    for arg_name, value in (
        ("person_name", person_name),
        ("user_bio", user_bio),
        ("status_message", status_message),
    ):
        if not isinstance(value, str):
            raise ValueError(f"{arg_name!r} must be a string")
        if not value.strip():
            raise ValueError(f"{arg_name!r} cannot be empty")

    # Escape user input to prevent XSS
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the provided template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)


# Example usage (would normally be removed or guarded by `if __name__ == "__main__":`)
if __name__ == "__main__":
    print(
        display_user_profile(
            "Alice <script>alert('xss')</script>",
            "I love coding. I also enjoy hiking & reading.",
            "Feeling great! 🚀",
        )
    )