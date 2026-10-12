import html

# Template for rendering a user profile on the web.
# The placeholders {username}, {biography} and {status} will be replaced
# with the escaped user input.
PROFILE_FORMAT: str = (
    "<div class='profile'>"
    "  <h1>{username}</h1>"
    "  <p>{biography}</p>"
    "  <footer><em>{status}</em></footer>"
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
        The profile string with all user input properly escaped to prevent
        Cross‑Site Scripting (XSS) attacks.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Validate input types
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(biography, str):
        raise ValueError("biography must be a string")
    if not isinstance(status, str):
        raise ValueError("status must be a string")

    # Escape user input to neutralize HTML/JS injection
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )