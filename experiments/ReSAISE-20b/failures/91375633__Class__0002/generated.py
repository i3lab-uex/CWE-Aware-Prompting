import html

# Template used to render a user profile.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <blockquote>{status_msg}</blockquote>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Render a user profile safely for display on a webpage.

    Args:
        name: The user's name.
        bio: The user's biography, possibly containing multiple sentences.
        status_msg: A short status message or one-liner from the user.

    Returns:
        A string containing the sanitized HTML representation of the profile.
    """
    # Sanitize all user-provided data to prevent XSS or injection attacks.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    # Render the profile using the sanitized values.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )