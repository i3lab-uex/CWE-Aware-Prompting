import html

# Predefined template for the user profile display.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a user's profile information for web display.

    The function sanitizes all user-supplied inputs to prevent HTML injection
    (CWE-74).  It uses the `html.escape` function which neutralizes special
    characters such as <, >, &, ", and '.

    Args:
        username (str): The user's name as entered.
        biography (str): A user-written biography that may span multiple sentences.
        status (str): A brief, current status message provided by the user.

    Returns:
        str: A formatted string containing the sanitized user profile information
             ready for web display.
    """
    # Escape all inputs to neutralize any HTML or script injection attempts.
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Construct the final profile string using the sanitized values.
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )