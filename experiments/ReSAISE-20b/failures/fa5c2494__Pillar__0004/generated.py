import html

# Predefined template for user profiles.
# The placeholders {name}, {bio}, and {status} will be replaced with sanitized values.
PROFILE_FORMAT: str = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <span class=\"status\">Status: {status}</span>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized user profile HTML snippet.

    Args:
        username: The user's full name.
        about: A multi-sentence biography provided by the user.
        current_status: A brief, current status update from the user.

    Returns:
        A string containing the sanitized and formatted user profile information.

    Raises:
        TypeError: If any argument is not a string.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(about, str):
        raise TypeError("about must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Sanitize inputs to prevent HTML injection (CWE-78, CWE-79)
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile