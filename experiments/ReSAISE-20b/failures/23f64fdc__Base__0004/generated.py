import html

# Predefined format for the user profile.  
# The placeholders are named to be compatible with str.format().
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h1>{username}</h1>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
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
        A potentially multi‑sentence user‑written biography.
    status : str
        A short, current status message.

    Returns
    -------
    str
        An HTML snippet with the user data safely escaped to prevent XSS.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be strings")

    # Escape user input to neutralize any embedded HTML or JavaScript
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )