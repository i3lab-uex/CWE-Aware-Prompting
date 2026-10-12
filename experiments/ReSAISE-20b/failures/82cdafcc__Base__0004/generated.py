import html

# Pre‑defined template for the user profile display.
# The placeholders are expected to be replaced by the
# sanitized values of name, bio and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    {status}\n"
    "  </div>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML representation of a user's profile.

    Parameters
    ----------
    person_name : str
        The name supplied by the user.
    user_bio : str
        A biography that may contain multiple sentences and arbitrary HTML characters.
    status_message : str
        A short status update.

    Returns
    -------
    str
        An HTML snippet with all user-supplied content properly escaped to prevent XSS.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types to avoid accidental injection of non‑string objects
    if not isinstance(person_name, str):
        raise TypeError("person_name must be a string")
    if not isinstance(user_bio, str):
        raise TypeError("user_bio must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape user input to neutralize any HTML or JavaScript
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)