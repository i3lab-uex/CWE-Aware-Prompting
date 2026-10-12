import html

# Predefined template for rendering a user profile.
# It contains placeholders that will be replaced with the sanitized data.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <div class=\"status\">{current_status}</div>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile information for safe web display.

    Parameters
    ----------
    fullname : str
        The user's full name as entered.
    biography : str
        A potentially multi‑sentence user biography.
    current_status : str
        The user's current status message.

    Returns
    -------
    str
        A sanitized, formatted HTML snippet ready for insertion into a web page.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types to avoid accidental injection of non‑string objects
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Escape all user‑supplied data to neutralize HTML/JS injection attempts.
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Render the profile using the predefined template.
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )