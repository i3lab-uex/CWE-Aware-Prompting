import html

# Pre‑defined template for the user profile display.
# The placeholders are named to make the format explicit and safe.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <div class=\"status\"><strong>Status:</strong> {status}</div>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized and formatted user profile for safe web display.

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
        The HTML snippet ready for rendering. All user‑supplied content is
        escaped to prevent XSS and injection attacks.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise TypeError("All arguments must be strings.")

    # Escape user‑supplied content to neutralize special HTML characters.
    escaped_name = html.escape(person_name, quote=True)
    escaped_bio = html.escape(user_bio, quote=True)
    escaped_status = html.escape(status_message, quote=True)

    # Format the profile using the safe placeholders.
    return PROFILE_FORMAT.format(
        name=escaped_name,
        bio=escaped_bio,
        status=escaped_status
    )