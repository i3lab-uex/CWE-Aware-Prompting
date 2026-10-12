import html

# Predefined template for rendering the user profile.
# Placeholders are named {name}, {bio} and {status}.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='biography'>{bio}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile information for web display.

    Parameters
    ----------
    fullname : str
        The user‑entered full name.
    biography : str
        A possibly multi‑sentence biography written by the user.
    current_status : str
        A short status message entered by the user.

    Returns
    -------
    str
        A sanitized, formatted HTML string ready for rendering in a web page.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Basic type checking to guard against accidental misuse
    if not all(isinstance(arg, str) for arg in (fullname, biography, current_status)):
        raise ValueError("All arguments must be strings.")

    # Escape all user‑supplied content to prevent XSS (CWE-79)
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )