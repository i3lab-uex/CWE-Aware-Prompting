import html

# Example profile template; in real use this would be defined elsewhere
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='biography'>{bio}</p>\n"
    "  <div class='status'>\u2022 {status}</div>\n"
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
        A user-provided biography that may contain multiple sentences.
    current_status : str
        A brief, current status message.

    Returns
    -------
    str
        The profile HTML with all user-supplied data escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (fullname, biography, current_status)):
        raise TypeError("All arguments must be of type str")

    # Escape user-provided data to prevent XSS
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )