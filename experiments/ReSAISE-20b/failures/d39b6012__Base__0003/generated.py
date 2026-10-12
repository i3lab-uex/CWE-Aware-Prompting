import html

# Predefined template for rendering a user profile on a web page.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <p class=\"status\"><strong>Status:</strong> {status}</p>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML snippet containing the user's profile.

    Args:
        user_name (str): The user's full name.
        biography (str): A multi-sentence biography provided by the user.
        status (str): The user's current brief status update.

    Returns:
        str: A string containing the sanitized and formatted user profile
             ready to be embedded in a web page.

    Raises:
        ValueError: If any of the arguments are not strings.
    """
    # Basic type checking
    if not isinstance(user_name, str):
        raise ValueError("user_name must be a string")
    if not isinstance(biography, str):
        raise ValueError("biography must be a string")
    if not isinstance(status, str):
        raise ValueError("status must be a string")

    # Escape user-supplied content to neutralize potential XSS payloads
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )