import html

# Pre‑defined template for the user profile.
PROFILE_FORMAT: str = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generates a sanitized HTML snippet representing the user's profile.

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
        The sanitized and formatted HTML profile string.
    """
    # Sanitize each user‑supplied field to prevent XSS and injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Safely format the profile using the sanitized values.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)