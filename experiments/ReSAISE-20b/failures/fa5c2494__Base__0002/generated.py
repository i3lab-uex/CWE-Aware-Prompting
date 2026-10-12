import html

# Pre‑defined template string for formatting user profiles.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <p class=\"status\"><strong>Status:</strong> {status}</p>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized HTML snippet for a user's profile.

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
        The sanitized and formatted HTML string ready for inclusion in a web page.

    Notes
    -----
    All user‑controlled input is escaped using html.escape to prevent XSS (CWE‑79).
    """
    # Escape all user inputs to neutralize potential HTML/JS injection.
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the sanitized data into the profile template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )