import html

# Template for rendering the user profile.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user-written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted HTML string containing the sanitized profile information.
    """
    # Escape user input to prevent XSS (CWE-79).
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )