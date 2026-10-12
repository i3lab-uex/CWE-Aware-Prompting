import html

# Template for displaying user profiles.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <blockquote class='status'>\"{status_msg}\"</blockquote>"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a user profile safely for display in HTML.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        The user's biography, which may contain multiple sentences.
    status_msg : str
        A short status message or one‑liner from the user.

    Returns
    -------
    str
        An HTML string with the profile data escaped to prevent XSS attacks.
    """
    # Escape all user input to avoid HTML injection
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )