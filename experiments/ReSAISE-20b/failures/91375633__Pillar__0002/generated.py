import html

# Template for displaying a user profile.
# Placeholders are replaced by sanitized values using `str.format`.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status_msg}</footer>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML string for displaying a user profile.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        A possibly multi‑sentence biography. May contain line breaks or HTML tags.
    status_msg : str
        A short one‑liner status message.

    Returns
    -------
    str
        An HTML fragment containing the profile, with all user‑supplied content escaped.

    Notes
    -----
    * The function escapes all user input to avoid XSS or other injection attacks.
    * `PROFILE_FORMAT` is a simple string template; it does not perform any advanced
      templating logic.
    """
    # Escape user input to neutralize HTML special characters.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_msg, quote=True)

    # Build the final profile string.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )