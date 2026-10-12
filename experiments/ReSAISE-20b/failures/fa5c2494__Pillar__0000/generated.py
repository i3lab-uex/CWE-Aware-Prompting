import html

# Pre‑defined template for a user profile.  
# It uses named placeholders to avoid accidental positional errors.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer class='status'>Status: {status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generates a sanitized HTML snippet representing a user profile.

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
        An HTML string with all user input safely escaped and inserted into
        PROFILE_FORMAT.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Input validation – ensure all inputs are strings
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(about, str):
        raise ValueError("about must be a string")
    if not isinstance(current_status, str):
        raise ValueError("current_status must be a string")

    # Escape all user‑supplied content to prevent XSS or markup injection.
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)