import html

# Predefined template for rendering the user profile.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
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
        A user‑written biography that may span multiple sentences.
    current_status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        A formatted string containing the sanitized profile information.
    """
    # Sanitize each user input to prevent XSS and ensure well‑formed HTML
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )
    return formatted_profile