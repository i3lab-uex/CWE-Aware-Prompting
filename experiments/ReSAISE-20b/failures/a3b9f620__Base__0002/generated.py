import html

# Example template: placeholders are {name}, {bio} and {status}
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer class='status'>Status: {status}</footer>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Build a safe HTML profile string from user input.

    Parameters
    ----------
    full_name : str
        The user's self-provided name.
    about_me : str
        A user-authored biography (may contain multiple sentences).
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted profile ready for web display.
    """
    # Sanitize all user-supplied fields to neutralize XSS vectors
    safe_name = html.escape(full_name, quote=True)
    safe_bio = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)