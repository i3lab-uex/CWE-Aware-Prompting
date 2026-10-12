import html

# Pre‑defined template string with placeholders for name, bio and status.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <p class='status'>Status: {status}</p>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML profile page from user input.

    Args:
        fullname: The user's full name.
        biography: A multi‑sentence biography provided by the user.
        status_message: A brief, current status update from the user.

    Returns:
        str: An HTML string containing the sanitized and formatted profile
             information.
    """
    # Validate that all arguments are strings
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape any HTML special characters to prevent XSS attacks
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the pre‑defined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )