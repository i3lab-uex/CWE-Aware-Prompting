import html

# Template used to format a user profile. The placeholders are named.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <blockquote>{status_msg}</blockquote>"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML representation of a user profile.

    Parameters
    ----------
    name : str
        The user's display name.
    bio : str
        A possibly multi‑sentence biography. May contain user input that
        should be escaped to prevent XSS.
    status_msg : str
        A short status message or one‑liner. Must also be escaped.

    Returns
    -------
    str
        A string containing the formatted, XSS‑safe HTML.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type validation
    if not all(isinstance(arg, str) for arg in (name, bio, status_msg)):
        raise TypeError("All arguments must be of type str")

    # Escape user supplied content to neutralize any HTML or script injection
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Format the profile string
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )