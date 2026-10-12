import html

# Example template; in real usage this would be defined elsewhere
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{username}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    {status_message}\n"
    "  </div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user profile safely for web display.

    Parameters
    ----------
    username : str
        The user's displayed name.
    bio : str
        A user-provided biography that may contain arbitrary text.
    status_message : str
        The user's current status update.

    Returns
    -------
    str
        A sanitized, HTML‑escaped profile string ready to be inserted into a page.
    """
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