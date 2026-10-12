import html

# Pre‑existing template for the user profile.  
# It uses `{name}`, `{bio}` and `{status}` as placeholders.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized user profile for web display.

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
        The profile string with all user input properly escaped to prevent XSS.
    """
    # Escape all user-supplied content to neutralize potential HTML/JS injection
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the sanitized data into the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)