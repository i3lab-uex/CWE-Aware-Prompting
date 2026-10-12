import html

# Template for the user profile.  The placeholders will be replaced by
# sanitized values to avoid injection vulnerabilities (CWE-74).
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\u2022 {status_msg}</div>\n"
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
        A short biography that may contain multiple sentences.
    status_msg : str
        A one‑liner status message.

    Returns
    -------
    str
        An HTML string with the user data safely escaped to prevent
        injection attacks (CWE‑74).
    """
    # Escape all user-provided content to neutralize any HTML/JS that
    # could be injected into the page.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    # Format the profile using the escaped values.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )