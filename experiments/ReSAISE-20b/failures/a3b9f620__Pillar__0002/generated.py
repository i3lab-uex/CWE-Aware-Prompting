import html

# Pre‑defined template for the user profile display.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"about-me\">{about_me}</p>\n"
    "  <div class=\"status-update\"><strong>Status:</strong> {status_update}</div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML representation of a user profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A biography written by the user. May contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A sanitized and formatted HTML snippet ready for web display.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checking to avoid unexpected input types
    if not isinstance(full_name, str):
        raise TypeError("full_name must be a string")
    if not isinstance(about_me, str):
        raise TypeError("about_me must be a string")
    if not isinstance(status_update, str):
        raise TypeError("status_update must be a string")

    # Escape user input to neutralize HTML/JS injection
    safe_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Format the profile using a well‑defined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )

    return formatted_profile