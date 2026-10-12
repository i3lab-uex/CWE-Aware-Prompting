import html

# Example profile format string; replace with the actual template in your application.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <div class='status'>Status: {status}</div>"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized user profile for safe web display.

    Args:
        person_name: The user's self-provided name.
        user_bio: A biography that may contain multiple sentences.
        status_message: A short, current status update.

    Returns:
        A string containing the sanitized and formatted user profile.
    """
    # Sanitize all user-supplied input to prevent XSS and injection attacks.
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )