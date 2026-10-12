import html

# Template for rendering a user profile on the web.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h1>{username}</h1>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status_message}</div>\n"
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
        A user-provided biography that may contain multiple sentences.
    status_message : str
        A short, current status message.

    Returns
    -------
    str
        The HTML string ready to be sent to the client, with all user input escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (username, bio, status_message)):
        raise TypeError("All arguments must be strings.")

    # Escape user input to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )