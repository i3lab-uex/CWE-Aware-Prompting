import html

# Predefined template for rendering a user profile on the web.
# The placeholders are {fullname}, {biography} and {current_status}.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h1>{fullname}</h1>"
    "  <p class='biography'>{biography}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {current_status}"
    "  </div>"
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
        A potentially multi‑sentence user biography.
    current_status : str
        The user's current status message.

    Returns
    -------
    str
        A fully escaped HTML string ready to be inserted into a page.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Validate argument types
    if not all(isinstance(arg, str) for arg in (fullname, biography, current_status)):
        raise ValueError("All arguments must be of type str")

    # Escape user supplied content to prevent XSS and other injection attacks.
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the final HTML string
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )