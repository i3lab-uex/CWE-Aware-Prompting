import html
from typing import Any


# A simple profile template with placeholders for name, bio and status.
PROFILE_FORMAT: str = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)


def _ensure_str(value: Any, name: str) -> str:
    """
    Ensure that the supplied value is a string.
    Raise TypeError if not.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized and formatted user profile page.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The HTML string containing the sanitized and formatted profile.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    """
    # Validate argument types
    fullname = _ensure_str(fullname, "fullname")
    biography = _ensure_str(biography, "biography")
    status_message = _ensure_str(status_message, "status_message")

    # Sanitize user-provided data to prevent XSS attacks
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)