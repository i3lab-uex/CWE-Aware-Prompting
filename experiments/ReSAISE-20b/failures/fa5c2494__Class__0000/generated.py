import html

# Pre‑defined template for the user profile.  
# It contains placeholders `{name}`, `{bio}` and `{status}`.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized and formatted user profile for display on a web page.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi‑sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The profile string with all user input escaped to prevent XSS and other injection attacks.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (username, about, current_status)):
        raise TypeError("All arguments must be of type str")

    # Escape user input to neutralize any HTML or script content
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)