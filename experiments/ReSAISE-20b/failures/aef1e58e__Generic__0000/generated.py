import html

# Predefined template for the user profile display.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class='biography'>{biography}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {current_status}\n"
    "  </div>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    fullname : str
        The user's full name as entered.
    biography : str
        A user-written biography that may contain multiple sentences.
    current_status : str
        A brief, current status message.

    Returns
    -------
    str
        A formatted string containing the sanitized user profile information.
    """
    # Basic validation: ensure all arguments are strings
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Escape HTML special characters to prevent XSS
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Construct the profile HTML
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )