import html

# Predefined template for the user profile. 
# The placeholders are named to avoid accidental injection via positional indices.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile string for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user-written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The formatted profile string with all user-supplied data HTML‑escaped.
    """
    # Escape all user-provided input to neutralize any HTML or script injection attempts.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )