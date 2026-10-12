import html

# Template for rendering the user profile on a web page.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{username}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status_message}\n"
    "  </div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user's profile for web display.

    The function sanitizes all user-supplied data to prevent
    Cross‑Site Scripting (XSS) attacks. It escapes special HTML
    characters before inserting the data into a predefined template.

    Args:
        username (str): The user's name as entered.
        bio (str): A user‑written biography that may span multiple sentences.
        status_message (str): A brief, current status message provided by the user.

    Returns:
        str: The sanitized and formatted HTML string ready for rendering on a web page.
    """
    # Escape user inputs to neutralize potential XSS payloads
    safe_username = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the sanitized data into the profile template
    return PROFILE_FORMAT.format(
        username=safe_username,
        bio=safe_bio,
        status_message=safe_status
    )