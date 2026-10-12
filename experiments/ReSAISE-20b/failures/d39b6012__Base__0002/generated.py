import html

# Predefined template for user profiles
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{biography}</p>"
    "  <footer>{status}</footer>"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized user profile for display on a web page.

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
        The sanitized and formatted user profile HTML snippet.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    """
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be of type str")

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