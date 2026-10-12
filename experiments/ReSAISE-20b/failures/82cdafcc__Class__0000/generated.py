import html

# Example template – the actual format may differ in the real application.
# Placeholders: {name}, {bio}, {status}
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Args:
        person_name (str): The user's self-provided name.
        user_bio (str): A biography that may contain multiple sentences.
        status_message (str): A short current status update.

    Returns:
        str: The sanitized and formatted user profile ready for web display.

    Raises:
        ValueError: If any argument is not a string.
    """
    # Basic type validation
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise ValueError("All arguments must be strings.")

    # Escape special HTML characters to prevent injection (CWE-74)
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )