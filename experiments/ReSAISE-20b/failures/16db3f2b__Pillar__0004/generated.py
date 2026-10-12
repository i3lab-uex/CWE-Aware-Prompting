import html

# Template for rendering a user profile on the web.
# It contains placeholders that will be safely substituted with escaped content.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer>{status_message}</footer>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile string for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user-written biography, possibly multi-sentence.
    status_message : str
        The user's current brief status update.

    Returns
    -------
    str
        A fully escaped and formatted HTML snippet ready for inclusion in a page.

    Raises
    ------
    ValueError
        If any of the required arguments is missing or not a string.
    """
    # Validate input types
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(bio, str):
        raise ValueError("bio must be a string")
    if not isinstance(status_message, str):
        raise ValueError("status_message must be a string")

    # Escape user-supplied content to prevent XSS and other injection attacks.
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using a trusted template.
    rendered = PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )
    return rendered