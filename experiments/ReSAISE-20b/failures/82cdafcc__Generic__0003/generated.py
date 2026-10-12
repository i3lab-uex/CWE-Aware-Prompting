import html

# Example template; in real use this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <p class='status'>Status: {status}</p>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML snippet for displaying a user profile.

    Parameters
    ----------
    person_name : str
        The user's self-provided name.
    user_bio : str
        A biography that may contain multiple sentences and HTML-like content.
    status_message : str
        A short current status update submitted by the user.

    Returns
    -------
    str
        An HTML-safe string containing the formatted profile information.
    """
    # Escape all user-provided content to prevent XSS attacks
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )