import html

# Example template with placeholders for name, about_me and status_update.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h1>{full_name}</h1>"
    "  <p class='about'>{about_me}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status_update}"
    "  </div>"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile HTML snippet.

    Args:
        full_name: The user's self-provided name.
        about_me: A user-authored biography (may contain multiple sentences).
        status_update: A short, current status update submitted by the user.

    Returns:
        A string containing the sanitized and formatted user profile information,
        ready for safe web display.

    Raises:
        TypeError: If any argument is not a string.
    """
    if not all(isinstance(arg, str) for arg in (full_name, about_me, status_update)):
        raise TypeError("All arguments must be strings")

    # Sanitize inputs to prevent injection (CWE-74)
    safe_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Build the profile using the predefined template
    profile_html = PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )

    return profile_html