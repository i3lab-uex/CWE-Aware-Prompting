import html

# Example template; in real usage this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{username}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>Status: {status_message}</div>\n"
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
        A user-written biography that may contain multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted string containing the sanitized profile ready for display.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or if PROFILE_FORMAT is not a string.
    """
    # Basic validation
    for arg_name, arg_value in (
        ("username", username),
        ("bio", bio),
        ("status_message", status_message),
    ):
        if not isinstance(arg_value, str):
            raise ValueError(f"{arg_name!r} must be a string")

    if not isinstance(PROFILE_FORMAT, str):
        raise ValueError("PROFILE_FORMAT must be a string template")

    # Escape user-provided content to prevent XSS and injection attacks
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile string
    try:
        rendered = PROFILE_FORMAT.format(
            username=safe_username,
            bio=safe_bio,
            status_message=safe_status
        )
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in PROFILE_FORMAT: {exc}") from None

    return rendered