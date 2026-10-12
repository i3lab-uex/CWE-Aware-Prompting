import html

# Predefined template for the user profile. The placeholders are named to match
# the arguments of `render_user_profile`.  No other processing is performed on
# this string so it can be safely used with `str.format`.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h1>{username}</h1>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status_message}</div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user's profile for safe web display.

    The function escapes all user-supplied input to neutralize HTML
    injection (CWE-74).  The escaping is performed using `html.escape`,
    which replaces &, <, >, ", and ' with their corresponding HTML entities.

    Parameters
    ----------
    username : str
        The user's display name.
    bio : str
        A biography that may contain multiple sentences and arbitrary characters.
    status_message : str
        The user's current status update.

    Returns
    -------
    str
        A fully escaped, formatted HTML snippet ready to be inserted into a page.
    """
    # Escape each user-provided string
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Use the predefined template to assemble the final string
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )