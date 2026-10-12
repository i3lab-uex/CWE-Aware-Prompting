import html

# Example template; in real usage this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's chosen name.
    biography : str
        A user‑written biography (may contain multiple sentences).
    status : str
        A brief, current status message.

    Returns
    -------
    str
        A formatted HTML string containing the sanitized profile information.
    """
    # Trim whitespace and escape any HTML special characters to prevent XSS
    safe_name = html.escape(username.strip())
    safe_bio = html.escape(biography.strip())
    safe_status = html.escape(status.strip())

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, biography=safe_bio, status=safe_status)