import html

# Template for the user profile display.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <blockquote class="status">{status_msg}</blockquote>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML snippet displaying the user's profile.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        The user's biography (may contain multiple sentences).
    status_msg : str
        A short status message or one‑liner from the user.

    Returns
    -------
    str
        An HTML string ready for inclusion in a web page. All user input is
        escaped to prevent XSS or other injection attacks.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Basic type checks to avoid unexpected behaviour
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(bio, str):
        raise ValueError("bio must be a string")
    if not isinstance(status_msg, str):
        raise ValueError("status_msg must be a string")

    # Escape user input to neutralise any malicious markup
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Construct the final HTML snippet
    profile_html = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )
    return profile_html.strip()