import html

# Template for displaying a user profile
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <span class='status'>Status: {status_msg}</span>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a sanitized user profile for display on a webpage.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        A possibly multi‑sentence biography.
    status_msg : str
        A short one‑liner status message.

    Returns
    -------
    str
        The profile HTML string with all user input escaped to prevent XSS.
    """
    # Escape all user‑provided content
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Construct the final HTML
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )