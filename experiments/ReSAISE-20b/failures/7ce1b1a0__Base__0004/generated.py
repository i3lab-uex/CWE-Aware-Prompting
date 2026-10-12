import html

# Pre‑defined template for the profile page.
# The placeholders `{username}`, `{biography}` and `{status}`
# will be replaced by the escaped user values.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='biography'>{biography}</p>\n"
    "  <div class='status'>\n"
    "    {status}\n"
    "  </div>\n"
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

    Notes
    -----
    All user input is escaped using `html.escape` to neutralise any
    potentially malicious content (CWE‑79: XSS).  No additional tags are
    allowed, and newlines in the biography or status are preserved as
    literal line breaks (converted to `<br>` tags by the browser).
    """
    # Escape all user‑supplied data.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Populate the template with escaped values.
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )