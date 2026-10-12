import html

# Example profile format template.
# It uses Python's format mini‑language with named placeholders.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{username}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <p class='status'><strong>Status:</strong> {status}</p>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    username : str
        The user's self‑provided name.
    biography : str
        A user‑authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A sanitized and formatted HTML snippet ready for safe web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checks
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status, str):
        raise TypeError("status must be a string")

    # Escape all user‑supplied content to avoid XSS attacks.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the provided template.
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )