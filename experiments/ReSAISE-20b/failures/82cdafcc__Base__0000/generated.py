import html

# Example template; in real use this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML profile display for the web interface.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A user‑authored biography that may contain multiple sentences.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted profile ready for safe web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    if not isinstance(person_name, str):
        raise TypeError("person_name must be a string")
    if not isinstance(user_bio, str):
        raise TypeError("user_bio must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape user input to prevent XSS (CWE‑79)
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Build the profile using the provided template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)