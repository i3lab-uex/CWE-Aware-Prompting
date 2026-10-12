import html

# Pre‑defined template for the profile page.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized and formatted user profile page.

    Args:
        fullname: The user's full name.
        biography: A multi‑sentence biography provided by the user.
        status_message: A brief, current status update from the user.

    Returns:
        A string containing the sanitized and formatted profile HTML.
    """
    # Sanitize all user‑supplied input to prevent XSS and injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)