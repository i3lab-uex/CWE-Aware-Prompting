import html

# Example profile format; replace with the actual template used by your web app.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='about-me'>{about_me}</p>\n"
    "  <div class='status-update'>\n"
    "    <strong>Status:</strong> {status_update}\n"
    "  </div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile string for safe web display.

    Parameters
    ----------
    full_name : str
        The user's self-provided name.
    about_me : str
        A user-authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile information,
        ready for safe web display.

    Raises
    ------
    ValueError
        If any of the arguments is not a string.
    """
    # Validate argument types
    if not isinstance(full_name, str):
        raise ValueError("full_name must be a string")
    if not isinstance(about_me, str):
        raise ValueError("about_me must be a string")
    if not isinstance(status_update, str):
        raise ValueError("status_update must be a string")

    # Escape user-supplied content to prevent XSS
    safe_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Format the profile using the provided template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )