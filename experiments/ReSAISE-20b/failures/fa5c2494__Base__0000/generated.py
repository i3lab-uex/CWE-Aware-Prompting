import html

# Predefined template for user profiles.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{about}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {current_status}"
    "  </div>"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generates a sanitized HTML snippet for a user profile.

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
        An HTML string containing the sanitized and formatted user profile.
    """
    # Escape all user-provided data to prevent XSS
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        current_status=safe_status
    )