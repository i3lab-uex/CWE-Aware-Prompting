import html

# Predefined template for user profiles.
# The placeholders {name}, {bio} and {status} will be replaced with
# sanitized user-provided values.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <p class='status'>Status: {status}</p>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile string for display on
    a web page.

    Parameters:
        user_name (str): The user's full name.
        biography (str): A multi-sentence biography provided by the user.
        status (str): A brief, current status update from the user.

    Returns:
        str: The sanitized and formatted HTML string containing the profile.
    """
    # Escape all user-supplied content to prevent injection of HTML/JS.
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template.
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile