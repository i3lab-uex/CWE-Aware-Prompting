import html

# Predefined template for rendering a user profile.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{username}</h2>
    <p class="bio">{bio}</p>
    <div class="status">{status_message}</div>
</div>
"""

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as they entered it.
    bio : str
        A user‑written biography that may span multiple sentences.
    status_message : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A sanitized, formatted string ready for embedding in HTML.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Basic type checks to avoid accidental injection of non‑string objects
    if not all(isinstance(arg, str) for arg in (username, bio, status_message)):
        raise ValueError("All arguments must be strings.")

    # Escape special HTML characters to prevent XSS or injection attacks.
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the template with sanitized values
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )