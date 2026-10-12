import html

# Pre‑defined template for the user profile. The placeholders are named
# "name", "bio" and "status". They will be replaced using str.format().
PROFILE_FORMAT: str = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <p class=\"status\"><strong>Status:</strong> {status}</p>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile HTML snippet.

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
        An HTML string containing the sanitized and formatted profile.

    Notes
    -----
    - All user input is escaped using :func:`html.escape` to prevent XSS
      attacks and other injection vulnerabilities.
    - The function does not perform any further validation (e.g. length
      checks) – that should be handled by the caller if required.
    """
    # Escape all user supplied data to avoid XSS
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status, quote=True)

    # Format the profile using the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)