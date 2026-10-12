import html

# Example template; in real usage this should be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{username}</h2>"
    "  <p class='biography'>{biography}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a safe HTML snippet representing the user's profile.

    Parameters
    ----------
    username : str
        The user-provided name.
    biography : str
        A potentially multi-sentence biography written by the user.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string containing the sanitized profile information,
        ready to be inserted into a web page.

    Notes
    -----
    All user input is escaped using html.escape to prevent cross‑site scripting (XSS).
    """
    # Escape all user-provided content
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )