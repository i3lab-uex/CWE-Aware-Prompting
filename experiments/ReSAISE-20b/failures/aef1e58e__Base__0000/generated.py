import html

# Predefined template for the user profile display.
# The placeholders {name}, {bio} and {status} will be replaced by the
# sanitized user-provided values.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h1>{name}</h1>"
    "  <p class='biography'>{bio}</p>"
    "  <div class='status'>Status: {status}</div>"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile for web display.

    The function sanitizes all user-provided input to prevent
    Cross‑Site Scripting (XSS) attacks by escaping HTML special characters.
    
    Args:
        fullname: The user's name as entered.
        biography: A multi‑sentence user-written biography.
        current_status: The user's brief current status message.

    Returns:
        A string containing the sanitized profile HTML ready for rendering.
    """
    # Escape all user input to neutralize any malicious code.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Populate the template with sanitized values.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)