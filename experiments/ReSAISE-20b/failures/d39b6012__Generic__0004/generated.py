import html
from typing import Any

# A pre‑defined template for rendering a user profile.
# It contains placeholders that will be replaced by the sanitized values.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>Status: {status}</div>\n"
    "</div>"
)


def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        A sanitized and formatted HTML string containing the user's profile information.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If any argument is an empty string after stripping whitespace.
    """
    # Type validation
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be of type str.")

    # Strip whitespace and check for emptiness
    stripped_name = user_name.strip()
    stripped_bio = biography.strip()
    stripped_status = status.strip()

    if not stripped_name:
        raise ValueError("user_name cannot be empty.")
    if not stripped_bio:
        raise ValueError("biography cannot be empty.")
    if not stripped_status:
        raise ValueError("status cannot be empty.")

    # Sanitize inputs to prevent XSS
    safe_name = html.escape(stripped_name)
    safe_bio = html.escape(stripped_bio).replace("\n", "<br>")
    safe_status = html.escape(stripped_status)

    # Format the profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )