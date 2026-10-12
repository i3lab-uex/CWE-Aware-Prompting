import html

# Pre‑defined template for rendering a user profile on the web page.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <p class=\"status\">Status: {status}</p>\n"
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
        An HTML string containing the escaped and formatted profile information.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(about, str):
        raise TypeError("about must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Escape user supplied data to prevent XSS
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True).replace("\n", "<br>")
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)