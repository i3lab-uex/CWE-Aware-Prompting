import html

# Template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <blockquote class='status'>{status_msg}</blockquote>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a user profile safely for inclusion in HTML.

    Parameters
    ----------
    name : str
        The user's display name.
    bio : str
        A potentially multi‑sentence biography. May contain user‑supplied
        content.
    status_msg : str
        A short one‑liner from the user.

    Returns
    -------
    str
        The HTML fragment containing the sanitized profile information.
    """
    # Escape user‑supplied content to prevent XSS attacks.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )