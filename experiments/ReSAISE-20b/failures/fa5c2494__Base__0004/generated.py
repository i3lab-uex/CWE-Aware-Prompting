import html

# Pre-defined template for the user profile.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{about}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi-sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted user profile information.
    """
    # Escape all user-provided content to mitigate XSS (CWE-79).
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        status=safe_status
    )