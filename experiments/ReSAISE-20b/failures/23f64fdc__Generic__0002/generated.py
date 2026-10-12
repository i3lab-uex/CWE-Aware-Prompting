import html

# Example profile template; placeholders are `{username}`, `{biography}` and `{status}`
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h2>{username}</h2>"
    "  <p class='bio'>{biography}</p>"
    "  <blockquote>{status}</blockquote>"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user profile for web display.

    Parameters
    ----------
    username : str
        The user's chosen name.
    biography : str
        A user‑written biographical text that may contain multiple sentences.
    status : str
        The user's current short status message.

    Returns
    -------
    str
        A sanitized, HTML‑escaped profile string ready for rendering.

    Raises
    ------
    ValueError
        If any of the arguments is None or not a string.
    """
    # Basic type checking
    for name, value in (("username", username), ("biography", biography), ("status", status)):
        if not isinstance(value, str):
            raise ValueError(f"Argument '{name}' must be a string")

    # Sanitize inputs to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined format
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )