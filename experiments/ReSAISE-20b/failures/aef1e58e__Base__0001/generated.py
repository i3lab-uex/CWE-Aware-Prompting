import html

# Predefined template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{biography}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user profile for web display.

    The function escapes all user-provided content to prevent
    Cross‑Site Scripting (CWE‑79) attacks. It then formats the
    PROFILE_FORMAT template with the sanitized values.

    Args:
        fullname: The user's full name as entered.
        biography: A user‑written biography that may contain multiple sentences.
        current_status: The user's brief, current status message.

    Returns:
        A sanitized HTML string ready to be embedded in a web page.
    """
    # Escape all user input
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Populate the template with sanitized values
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )