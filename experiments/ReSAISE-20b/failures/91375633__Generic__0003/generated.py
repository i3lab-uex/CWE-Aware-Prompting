import html

# Template used to render the user profile.  The placeholders are
# ``{name}``, ``{bio}`` and ``{status_msg}``.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <p class='status'>Status: {status_msg}</p>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML snippet that displays a user profile.

    Parameters
    ----------
    name : str
        The user's display name.
    bio : str
        A possibly multi‑sentence biography.  May contain user input that
        should be escaped.
    status_msg : str
        A short one‑liner status message.  Also must be escaped.

    Returns
    -------
    str
        The concatenated, HTML‑escaped profile string ready for rendering.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    if not all(isinstance(arg, str) for arg in (name, bio, status_msg)):
        raise TypeError("All arguments must be of type str")

    # Escape user supplied data to prevent XSS attacks.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )