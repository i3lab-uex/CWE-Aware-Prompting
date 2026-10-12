import html

# Example profile format template.
# The placeholders `{name}`, `{bio}` and `{status}` will be replaced
# with the sanitized user supplied values.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
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
        A sanitized and formatted HTML string ready for safe web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be strings")

    # Escape special HTML characters to prevent injection (CWE‑74)
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the template with sanitized values
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )