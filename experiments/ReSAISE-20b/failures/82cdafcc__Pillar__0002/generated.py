import html

# Pre‑defined template for the user profile display.
# The placeholders {name}, {bio} and {status} will be replaced with
# the sanitized user data.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <p class=\"status\">Status: {status}</p>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML representation of a user profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        The user's current short status update.

    Returns
    -------
    str
        A sanitized and formatted HTML string ready for web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If the status message exceeds 200 characters (arbitrary limit for safety).
    """
    # Basic type checking
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise TypeError("All arguments must be strings")

    # Optional length check to guard against very large inputs
    if len(status_message) > 200:
        raise ValueError("Status message too long (max 200 characters)")

    # Escape all user‑supplied content to neutralise HTML/JS injection
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using a format string that has been escaped
    rendered = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return rendered