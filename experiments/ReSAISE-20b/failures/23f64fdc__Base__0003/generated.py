import html

# Predefined template for user profiles.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{username}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <footer class='status'>Status: {status}</footer>\n"
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
        A multi‑sentence user biography.
    status : str
        A short current status message.

    Returns
    -------
    str
        The HTML snippet containing the profile information, safely escaped.
    """
    # Escape all user input to neutralize potential XSS payloads.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )