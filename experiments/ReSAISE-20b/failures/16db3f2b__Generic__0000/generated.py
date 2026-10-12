import html

# Predefined template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's entered name.
    bio : str
        A user-written biography that may contain multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted string containing sanitized user profile information ready for web display.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Basic type validation
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(bio, str):
        raise ValueError("bio must be a string")
    if not isinstance(status_message, str):
        raise ValueError("status_message must be a string")

    # Sanitize inputs to prevent XSS or HTML injection
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=False).replace("\n", "<br>")
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the predefined template
    rendered = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return rendered