import html

# Predefined template for rendering the user profile.
# The placeholders are `{name}`, `{bio}` and `{status}`.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile for web display.

    The function escapes all user-provided input to prevent HTML injection
    (CWE-74). It then substitutes the sanitized values into a predefined
    template.

    Args:
        fullname: The user's name as entered.
        biography: A user-written biography (may contain multiple sentences).
        current_status: A brief, current status message.

    Returns:
        A sanitized HTML string containing the formatted user profile.
    """
    # Escape special characters to neutralize potential injection vectors
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the sanitized values into the profile template
    rendered = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return rendered