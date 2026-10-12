import html

# Pre-defined template for a user profile.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <span class='status'>Status: {status}</span>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted HTML string ready to be embedded in a web page.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be strings")

    # Escape user-provided content to prevent XSS (CWE-79)
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )