import html

# Pre‑defined template for the profile.  The placeholders are named to match the
# arguments passed to `generate_user_profile`.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"about-me\">{bio}</p>\n"
    "  <div class=\"status-update\">{status}</div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML snippet containing the user's profile information.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A biography that may contain multiple sentences.  May include user‑supplied text.
    status_update : str
        A short, current status message.

    Returns
    -------
    str
        The profile rendered using PROFILE_FORMAT with all user input escaped to prevent XSS.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types to avoid unexpected errors later
    if not all(isinstance(arg, str) for arg in (full_name, about_me, status_update)):
        raise TypeError("All arguments must be strings")

    # Escape user input to prevent injection of HTML/JS
    safe_name = html.escape(full_name, quote=True)
    safe_bio = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)