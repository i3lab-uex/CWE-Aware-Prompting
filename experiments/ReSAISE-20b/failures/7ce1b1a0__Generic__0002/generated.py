import html

# Example format string; in real usage this should be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{username}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    username : str
        The user's self-provided name.
    biography : str
        A user-authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted HTML ready for safe web display.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise ValueError("All arguments must be strings.")

    # Escape all user-supplied content to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format using the predefined template
    rendered_profile = PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )
    return rendered_profile