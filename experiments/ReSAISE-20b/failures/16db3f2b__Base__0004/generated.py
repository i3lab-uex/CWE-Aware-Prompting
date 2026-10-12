import html

# Predefined template for rendering the user profile.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{username}</h2>
    <p class="bio">{bio}</p>
    <div class="status">
        <strong>Status:</strong> {status_message}
    </div>
</div>
"""

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user-written biography, possibly spanning multiple sentences.
    status_message : str
        A brief current status message.

    Returns
    -------
    str
        The profile HTML with all user-supplied content escaped to prevent XSS.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (username, bio, status_message)):
        raise ValueError("All arguments must be strings")

    # Escape user input to neutralize any potential XSS payloads
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the sanitized data into the template
    rendered = PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )
    return rendered.strip()