import html

# Predefined template for user profiles.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <p class='status'><em>{status}</em></p>\n"
    "</div>"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generates a sanitized and formatted user profile string for display on a web page.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted user profile HTML snippet.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or are empty.
    """
    # Validate input types and non-emptiness
    for arg_name, value in (("user_name", user_name), ("biography", biography), ("status", status)):
        if not isinstance(value, str):
            raise ValueError(f"{arg_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{arg_name} cannot be empty or whitespace only.")

    # Escape user-supplied content to prevent XSS and other injection attacks
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile