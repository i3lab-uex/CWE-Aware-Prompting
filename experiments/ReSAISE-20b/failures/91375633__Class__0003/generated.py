import html

# Template for displaying a user profile.  The placeholders will be filled with the
# sanitized user data.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <div class="status">{status_msg}</div>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a user profile safely for inclusion in an HTML page.

    Parameters
    ----------
    name : str
        The user's display name.
    bio : str
        A potentially multi‑sentence biography.  May contain HTML special characters.
    status_msg : str
        A short one‑liner or status message.  May contain HTML special characters.

    Returns
    -------
    str
        The fully formatted, escaped profile markup ready for rendering in a browser.

    Notes
    -----
    All user input is escaped using :func:`html.escape` to neutralise characters that
    could otherwise break the HTML structure or be interpreted as markup, mitigating
    CWE‑74 (improper neutralisation of special elements in output used by a downstream component).
    """
    # Escape user input to avoid injection of HTML or script tags.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    # Format the profile using the sanitized values.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )