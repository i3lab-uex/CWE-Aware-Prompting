import html

# Pre‑defined template with placeholders for name, biography and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized HTML snippet for displaying a user's profile.

    Parameters
    ----------
    username : str
        The user-provided name.
    biography : str
        A potentially multi‑sentence biography written by the user.
    status : str
        The user's current short status update.

    Returns
    -------
    str
        A string containing the sanitized and formatted profile ready for safe web display.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise ValueError("All arguments must be strings")

    # Escape all user input to neutralize XSS vectors
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )