import html

# Pre‑defined profile template with placeholders for name, biography and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='biography'>{biography}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized user profile HTML snippet.

    Args:
        username: The user's self‑provided name.
        biography: A multi‑sentence user‑authored biography.
        status: A short, current status update.

    Returns:
        A string containing the HTML snippet with all user input safely escaped.
    """
    # Escape all user supplied data to prevent XSS (CWE‑79).
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the template with the escaped values.
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )