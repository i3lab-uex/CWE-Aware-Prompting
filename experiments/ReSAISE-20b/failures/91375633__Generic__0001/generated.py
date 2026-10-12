import html

# Template used for rendering the user profile on a webpage.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <blockquote>{status_msg}</blockquote>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a user profile as an HTML snippet.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        A potentially multi‑sentence biography of the user.
    status_msg : str
        A short status message or one‑liner from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized profile information.

    Notes
    -----
    The function sanitizes all user‑supplied input using `html.escape`
    to prevent XSS attacks.  It does not perform any additional
    validation on the content of the strings.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Format the profile using the template
    rendered_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )

    return rendered_profile