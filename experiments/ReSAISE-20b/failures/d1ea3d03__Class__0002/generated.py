import html

# Pre‑defined template for user profiles.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <span class='status'>Status: {status}</span>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML profile page for a user.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        Sanitized and formatted HTML containing the user's profile.
    """
    # Escape all user supplied content to avoid injection attacks (CWE‑74).
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )