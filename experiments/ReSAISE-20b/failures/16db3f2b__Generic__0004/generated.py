import html
from typing import Any

# Predefined template for rendering the user profile.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status_message}\n"
    "  </div>\n"
    "</div>"
)


def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user‑written biography that may contain multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The profile HTML string with all user data escaped to prevent XSS.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate argument types
    for name, value in (("username", username), ("bio", bio), ("status_message", status_message)):
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string, got {type(value).__name__}")

    # Escape user inputs to mitigate XSS attacks
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    rendered = PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )

    return rendered