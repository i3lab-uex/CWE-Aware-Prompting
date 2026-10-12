import html

# Template for the user profile page.
# Use named placeholders for clarity and safety.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{username}</h2>
    <p class="bio">{bio}</p>
    <div class="status"><strong>Status:</strong> {status_message}</div>
</div>
"""

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    bio : str
        A user-written biography that may contain multiple sentences.
    status_message : str
        The user's current status update.

    Returns
    -------
    str
        A sanitized HTML string ready to be inserted into a web page.

    Notes
    -----
    All user input is escaped using :func:`html.escape` to prevent XSS
    (CWE‑79).  No user-supplied data is evaluated as code or parsed as
    HTML.  The function only performs string formatting with the escaped
    values.
    """
    # Escape all user-provided strings to neutralize HTML/JS injection.
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the sanitized values.
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )