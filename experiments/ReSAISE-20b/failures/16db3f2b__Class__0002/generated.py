import html

# Predefined template for the user profile display.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user‑written biography that may span multiple sentences.
    status_message : str
        A brief, current status message.

    Returns
    -------
    str
        A formatted string containing the sanitized user profile information,
        safe for inclusion in HTML.
    """
    # Escape any special characters to prevent HTML injection (CWE-74).
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=False)  # Preserve line breaks if any
    safe_status = html.escape(status_message, quote=True)

    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)