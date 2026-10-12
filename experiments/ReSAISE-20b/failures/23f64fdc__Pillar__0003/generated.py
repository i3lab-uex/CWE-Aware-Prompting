import html

# Template for rendering the user profile.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <footer class='status'>Status: {status}</footer>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user-written biography that may contain multiple sentences.
    status : str
        A brief, current status message.

    Returns
    -------
    str
        The profile HTML string with all user input properly escaped to prevent
        XSS or other injection attacks.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Basic type checking to avoid unexpected input
    if not isinstance(username, str):
        raise ValueError("username must be a string")
    if not isinstance(biography, str):
        raise ValueError("biography must be a string")
    if not isinstance(status, str):
        raise ValueError("status must be a string")

    # Escape user-provided content to neutralize malicious code
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )