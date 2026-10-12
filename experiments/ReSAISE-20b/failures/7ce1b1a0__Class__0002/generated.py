import html

# Pre‑defined template for the user profile.  The placeholders are
# intentionally named to match the function arguments.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized and formatted user profile string for safe web display.

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
        The profile string with all user input escaped to prevent HTML injection.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types early to avoid accidental injection through non‑string objects
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status, str):
        raise TypeError("status must be a string")

    # Escape all user‑supplied content to neutralize special characters that could
    # otherwise alter the HTML structure or inject scripts.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the final output using the predefined template.
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )