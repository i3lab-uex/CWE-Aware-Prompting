import html
from typing import Final

# Example profile format template. The placeholders should match the arguments.
PROFILE_FORMAT: Final[str] = (
    "<div class='user-profile'>"
    "  <h1>{fullname}</h1>"
    "  <p class='biography'>{biography}</p>"
    "  <div class='status'>Status: {current_status}</div>"
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
        A user-provided biographical description, possibly multiline.
    current_status : str
        The user's brief status message.

    Returns
    -------
    str
        A sanitized, formatted HTML string ready for rendering on a web page.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (fullname, biography, current_status)):
        raise ValueError("All arguments must be strings.")

    # Escape user content to prevent XSS
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(current_status, quote=True)

    # Format the profile
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )