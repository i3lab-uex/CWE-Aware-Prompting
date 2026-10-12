import html

# Template for the profile display; placeholders use Python's format syntax.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{username}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status_message}"
    "  </div>"
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
        A user-written biography that may span multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The profile HTML string with all user-provided content escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(bio, str):
        raise TypeError("bio must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape all user input to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )