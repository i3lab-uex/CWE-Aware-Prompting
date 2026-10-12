import html

# Predefined template for the profile display.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='biography'>{biography}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
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
        The user's current status message.

    Returns
    -------
    str
        A formatted HTML string containing the sanitized profile information.

    Notes
    -----
    - All user‑supplied data is HTML‑escaped to prevent injection attacks.
    - The function does not perform any further validation of the content beyond
      escaping, which is sufficient for most display scenarios.
    """
    # Escape all user input to neutralize HTML injection
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined template
    rendered_profile = PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )
    return rendered_profile