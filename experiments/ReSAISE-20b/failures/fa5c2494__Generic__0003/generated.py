import html

# Pre‑defined template for user profiles.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <span class='status'>Status: {status}</span>\n"
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
        The HTML string containing the sanitized profile information.

    Notes
    -----
    - All user input is escaped to prevent XSS attacks.
    - Leading/trailing whitespace is stripped from each field.
    """
    # Sanitize and trim input
    name = html.escape(username.strip())
    bio = html.escape(about.strip())
    status = html.escape(current_status.strip())

    # Format using the predefined template
    return PROFILE_FORMAT.format(name=name, bio=bio, status=status)