import html

# Template used to render a user profile.  The placeholders are replaced by
# the sanitized values supplied to ``show_user_profile``.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <blockquote>{status_msg}</blockquote>"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML snippet that displays the user's profile.

    Parameters
    ----------
    name : str
        The user’s display name.
    bio : str
        A potentially multi‑sentence biography.  May contain user supplied
        characters that need to be escaped.
    status_msg : str
        A short status message or one‑liner.

    Returns
    -------
    str
        An HTML string with the user data safely escaped to avoid XSS.

    Notes
    -----
    The function uses :func:`html.escape` to neutralise any HTML special
    characters in the user input.  This protects against CWE‑79
    (Cross‑Site Scripting) by ensuring that no injected markup can be executed
    when the resulting string is inserted into a page.

    Examples
    --------
    >>> show_user_profile('Alice', 'Hello <world>', 'Enjoying coding!')
    "<div class='user-profile'><h2>Alice</h2><p class='bio'>Hello &lt;world&gt;</p><blockquote>Enjoying coding!</blockquote></div>"
    """
    # Escape user input to prevent HTML injection
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_msg, quote=True)

    # Render the template with the sanitized values
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )