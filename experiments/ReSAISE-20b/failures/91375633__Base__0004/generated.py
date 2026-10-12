import html

# Template for displaying a user profile.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer>{status_msg}</footer>\n"
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
        A potentially multi‑sentence biography.
    status_msg : str
        A short status message or one‑liner.

    Returns
    -------
    str
        An HTML string with all user input safely escaped.
    """
    # Escape all user‑controlled data to prevent XSS attacks (CWE‑79).
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )