import html

# Predefined template for rendering a user profile.
# The placeholders are named 'fullname', 'biography', and 'status'.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{fullname}</h2>"
    "  <p class='bio'>{biography}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile for web display.

    The function sanitizes all user-supplied input to prevent
    cross‑site scripting (XSS) attacks by escaping HTML special
    characters.

    Parameters:
        fullname (str): The user's full name.
        biography (str): A multi‑sentence user biography.
        current_status (str): The user's current status message.

    Returns:
        str: A sanitized, formatted HTML string ready for rendering.
    """
    # Escape user input to neutralize any embedded HTML or JavaScript
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        status=safe_status
    )