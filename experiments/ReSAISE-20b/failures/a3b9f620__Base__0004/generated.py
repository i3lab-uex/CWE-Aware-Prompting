import html

# Example template with placeholders for name, about_me and status_update.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{full_name}</h2>\n"
    "  <p class='bio'>{about_me}</p>\n"
    "  <div class='status'>Status: {status_update}</div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    full_name : str
        The user's self-provided name.
    about_me : str
        A user-authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A sanitized and formatted string ready for safe web display.
    """
    # Escape all user-supplied content to prevent XSS attacks (CWE-79).
    safe_name = html.escape(full_name, quote=True)
    safe_bio = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the provided template.
    return PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_bio,
        status_update=safe_status
    )