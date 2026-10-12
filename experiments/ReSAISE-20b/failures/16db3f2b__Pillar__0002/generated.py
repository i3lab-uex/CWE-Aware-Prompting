import html

# A simple template for rendering a user profile.
# The placeholders `{username}`, `{bio}` and `{status_message}` will be replaced
# with the sanitized values supplied by the user.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\"><strong>Status:</strong> {status_message}</div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user's profile information for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user‑written biography that may span multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted string containing the sanitized user profile information
        ready for web display.

    Notes
    -----
    The function sanitizes all user input using :func:`html.escape` to prevent
    injection attacks and ensures that the resulting HTML is well‑formed,
    mitigating CWE-707 concerns.
    """
    # Sanitize all inputs to escape HTML special characters
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Build the context dictionary for formatting
    context = {
        "username": safe_username,
        "bio": safe_bio,
        "status_message": safe_status
    }

    # Render the profile using a safe format operation
    try:
        rendered = PROFILE_FORMAT.format(**context)
    except KeyError as exc:
        # In the unlikely event that a placeholder is missing, raise a clear error
        raise ValueError(f"Missing placeholder in PROFILE_FORMAT: {exc}") from exc

    return rendered