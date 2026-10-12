import html
from typing import Any

# Pre‑defined template for rendering the user profile on a web page.
# The placeholders are :name:, :bio: and :status:.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\u2022 {status}</div>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML snippet containing the user's profile.

    Parameters
    ----------
    user_name : str
        The full name of the user.
    biography : str
        A multi‑sentence biography supplied by the user.
    status : str
        A short, current status update.

    Returns
    -------
    str
        An HTML string with the profile data safely escaped and formatted.

    Raises
    ------
    TypeError
        If any of the arguments is not a string.
    ValueError
        If any argument is an empty string after stripping whitespace.
    """
    # Validate input types
    for arg_name, arg_value in (
        ("user_name", user_name),
        ("biography", biography),
        ("status", status),
    ):
        if not isinstance(arg_value, str):
            raise TypeError(f"{arg_name} must be a string, got {type(arg_value).__name__}")

    # Strip whitespace and check for emptiness
    if not user_name.strip():
        raise ValueError("user_name cannot be empty or whitespace only")
    if not biography.strip():
        raise ValueError("biography cannot be empty or whitespace only")
    if not status.strip():
        raise ValueError("status cannot be empty or whitespace only")

    # Escape HTML special characters to prevent XSS
    safe_name = html.escape(user_name.strip())
    safe_bio = html.escape(biography.strip()).replace("\n", "<br>")
    safe_status = html.escape(status.strip())

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)