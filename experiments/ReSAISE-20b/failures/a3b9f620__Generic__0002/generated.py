import html

# Example profile format template.
# The placeholders {name}, {about_me} and {status} will be replaced
# by the sanitized user inputs.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='about-me'>{about_me}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile string ready for safe HTML display.

    Args:
        full_name: The user's self-provided name.
        about_me: A user-authored biography that may contain multiple sentences.
        status_update: A short, current status update submitted by the user.

    Returns:
        A string containing the sanitized and formatted profile HTML.
    """
    # Sanitize all inputs to prevent XSS or injection attacks
    safe_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about_me=safe_about_me,
        status=safe_status
    )