import html

# Template for the user profile; placeholders are marked with {name}, {bio}, and {status}
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="biography">{bio}</p>
    <blockquote class="status">{status}</blockquote>
</div>
"""

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user's profile information safely for web display.

    Parameters
    ----------
    username : str
        The user's name as they entered it.
    biography : str
        A user‑written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The profile HTML string with all user input properly escaped to prevent
        injection attacks (CWE‑74).
    """
    # Escape all user-provided content to neutralize special HTML characters
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)