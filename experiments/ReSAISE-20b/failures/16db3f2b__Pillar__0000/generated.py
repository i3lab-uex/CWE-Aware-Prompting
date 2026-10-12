import html

# Predefined template for rendering a user profile.
# Placeholders: {username}, {bio}, {status_message}
PROFILE_FORMAT = (
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
        A potentially multi‑sentence biography written by the user.
    status_message : str
        A brief current status message.

    Returns
    -------
    str
        An HTML string containing the sanitized user profile.
    """
    # Escape all inputs to prevent XSS and ensure well‑formedness
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )