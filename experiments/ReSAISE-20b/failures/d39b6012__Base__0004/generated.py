import html

# Pre-defined template string for formatting user profiles.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized user profile HTML snippet.

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
        The sanitized and formatted HTML snippet for the user's profile.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status, str):
        raise TypeError("status must be a string")

    # Escape user-provided content to prevent XSS (CWE-79)
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )