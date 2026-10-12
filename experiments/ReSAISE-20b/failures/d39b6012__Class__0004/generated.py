import html

# Pre‑defined template for user profiles.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile for display on a web page.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted HTML string representing the user profile.
    """
    # Escape all user‑supplied content to prevent XSS and template injection.
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the template.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)