import html

# Example template; in real usage this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{full_name}</h2>\n"
    "  <p class='about'>{about_me}</p>\n"
    "  <div class='status'>Status: {status_update}</div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile for safe web display.

    Args:
        full_name (str): The user's self-provided name.
        about_me (str): A user-authored biography that may contain multiple sentences.
        status_update (str): A short, current status update submitted by the user.

    Returns:
        str: The formatted and HTML-escaped profile string ready for rendering in a browser.

    Raises:
        TypeError: If any argument is not a string.
    """
    if not all(isinstance(arg, str) for arg in (full_name, about_me, status_update)):
        raise TypeError("All arguments must be strings")

    # Escape user input to prevent XSS (CWE-79)
    safe_full_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    return PROFILE_FORMAT.format(
        full_name=safe_full_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )