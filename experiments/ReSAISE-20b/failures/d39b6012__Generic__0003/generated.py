import html

# Predefined template for the user profile.
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
        A sanitized and formatted HTML string containing the profile information.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If any of the arguments are empty after stripping whitespace.
    """
    # Validate types
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be of type str.")

    # Strip whitespace and check for emptiness
    if not user_name.strip():
        raise ValueError("user_name cannot be empty.")
    if not biography.strip():
        raise ValueError("biography cannot be empty.")
    if not status.strip():
        raise ValueError("status cannot be empty.")

    # Escape user-provided content to prevent XSS
    safe_name = html.escape(user_name.strip(), quote=True)
    safe_bio = html.escape(biography.strip(), quote=False).replace("\n", "<br>")
    safe_status = html.escape(status.strip(), quote=True)

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )

    return formatted_profile