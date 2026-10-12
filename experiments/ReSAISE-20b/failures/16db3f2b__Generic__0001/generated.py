import html

# Example profile format template.
# The placeholders must match the keyword arguments used in the function below.
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
        The user's name as entered.
    bio : str
        A potentially multi‑sentence biography written by the user.
    status_message : str
        A short, current status message.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering on a web page.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or not strings.
    """
    # Validate inputs
    if not all(isinstance(arg, str) for arg in (username, bio, status_message)):
        raise ValueError("All arguments must be strings.")

    # Escape HTML special characters to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the predefined format
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )