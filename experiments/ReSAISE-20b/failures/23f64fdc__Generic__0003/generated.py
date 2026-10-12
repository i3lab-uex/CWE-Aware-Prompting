import html

# Template used for rendering a user profile.
# It contains placeholders that will be replaced by the
# sanitized username, biography and status message.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user's profile information for web display.

    Parameters
    ----------
    username : str
        The user's name as they entered it.
    biography : str
        A user-written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted string containing the sanitized user profile information
        ready for web display.

    Raises
    ------
    TypeError
        If any of the arguments are not strings.
    """
    # Validate argument types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status, str):
        raise TypeError("status must be a string")

    # Escape user-provided data to prevent XSS attacks.
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined format.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)