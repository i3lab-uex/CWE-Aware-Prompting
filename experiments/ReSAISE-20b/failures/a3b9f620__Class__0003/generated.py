import html

# Predefined profile template with placeholders for name, biography and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{about_me}</p>\n"
    "  <footer>{status_update}</footer>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe user profile display string.

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
        The sanitized and formatted user profile ready for safe web display.

    Raises
    ------
    ValueError
        If any of the inputs is not a string.
    """
    # Basic type validation
    if not all(isinstance(arg, str) for arg in (full_name, about_me, status_update)):
        raise ValueError("All arguments must be strings.")

    # Escape HTML special characters to prevent injection attacks (CWE-74)
    safe_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )