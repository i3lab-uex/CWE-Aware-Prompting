import html

# Predefined template for user profiles
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{about}</p>\n"
    "  <footer class='status'>Status: {status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generates a sanitized HTML snippet for displaying a user profile.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi-sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted profile information.
    """
    # Sanitize user input to prevent XSS attacks
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        status=safe_status
    )