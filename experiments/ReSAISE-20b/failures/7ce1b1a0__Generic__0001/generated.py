import html

# Example template for the profile display.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a safe HTML representation of a user's profile.

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
        The sanitized and formatted profile HTML string, ready for safe web display.

    Notes
    -----
    - All user‑supplied content is escaped using html.escape to prevent XSS attacks.
    - The function does not perform any length checks; if required, callers should
      validate input size before calling this function.
    """
    # Escape user inputs to prevent injection attacks
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    rendered_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )
    return rendered_profile