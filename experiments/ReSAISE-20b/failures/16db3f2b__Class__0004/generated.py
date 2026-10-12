import html

# Define a template for rendering the profile.
# The placeholders are {name}, {bio}, and {status}.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\"><strong>Status:</strong> {status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, bio: str, status_message: str) -> str:
    """
    Render a user profile for web display.

    The function escapes all user-supplied content to prevent
    HTML injection (CWE‑74). It returns a string that can be safely
    inserted into an HTML document.

    Args:
        username (str): The user's display name.
        bio (str): A multi‑sentence biography written by the user.
        status_message (str): The user's current status message.

    Returns:
        str: A sanitized, formatted profile string.
    """
    # Escape all user-provided data
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the template with sanitized values
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)