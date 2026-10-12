import html

# Pre‑defined template for user profiles.  
# The placeholders will be replaced by the sanitized values.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <p class='status'><em>{status}</em></p>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML user profile from the supplied data.

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

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be of type 'str'")

    # Sanitize each component to prevent HTML injection (CWE‑74)
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the final profile string
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)