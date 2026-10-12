import html

# Predefined template for the user profile. 
# Replace {name}, {biography}, and {status} with actual values.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{biography}</p>\n"
    "  <p class='status'>Status: {status}</p>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's entered name.
    biography : str
        A potentially multi‑sentence user biography.
    status : str
        A short current status message.

    Returns
    -------
    str
        The profile HTML string with user data safely escaped.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )