import html

# Predefined template for rendering the profile.
# Example: "<h1>{name}</h1><p>{bio}</p><div class='status'>{status}</div>"
PROFILE_FORMAT = "<h1>{name}</h1><p>{bio}</p><div class='status'>{status}</div>"

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user's profile information safely for web display.

    Parameters
    ----------
    username : str
        The user-entered name.
    bio : str
        A potentially multi-sentence biography written by the user.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The formatted profile string with all content HTML-escaped to avoid
        injection attacks (CWE‑707).

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(bio, str):
        raise TypeError("bio must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Sanitize all user-provided content to neutralize potential HTML/JS injection
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)