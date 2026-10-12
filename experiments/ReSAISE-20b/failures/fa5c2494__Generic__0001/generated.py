import html

# Pre‑defined template for the user profile display.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{about}</p>\n"
    "  <p class='status'>Status: {current_status}</p>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized HTML snippet for displaying a user profile.

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
        The sanitized and formatted HTML string ready for embedding in a web page.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(about, str):
        raise TypeError("about must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Escape all user input to avoid XSS or HTML injection
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        current_status=safe_status
    )