import html

# Predefined profile template
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
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
        A user‑written biographical description (may contain multiple sentences).
    status : str
        The user's current brief status message.

    Returns
    -------
    str
        A formatted HTML string containing the sanitized profile information.
    """
    # Escape all user input to prevent XSS and other injection attacks
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)