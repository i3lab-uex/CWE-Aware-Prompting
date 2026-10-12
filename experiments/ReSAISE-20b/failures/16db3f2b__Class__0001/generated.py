import html

# Predefined template for the user profile.  The placeholders will be filled
# with escaped values to avoid injection attacks such as XSS.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>\n"
    "  <h1>{username}</h1>\n"
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
        The user's name as they entered it.
    bio : str
        A user‑written biography that may span multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The formatted HTML string with all user input properly escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types to avoid accidental injection via non‑string objects
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(bio, str):
        raise TypeError("bio must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape all user input to neutralize HTML special characters
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the template with escaped values
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )