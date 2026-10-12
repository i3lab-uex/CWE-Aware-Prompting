import html

# Template used to render the user profile on a webpage.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <blockquote class="status">{status_msg}</blockquote>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a sanitized user profile suitable for embedding in an HTML page.

    Parameters
    ----------
    name : str
        The user's display name.
    bio : str
        A potentially multi‑sentence biography. May contain line breaks or HTML‑like text.
    status_msg : str
        A short one‑liner status message.

    Returns
    -------
    str
        The profile HTML with all user input safely escaped to prevent XSS.
    """
    # Escape user‑controlled input to neutralize any HTML/JS content
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_msg, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )