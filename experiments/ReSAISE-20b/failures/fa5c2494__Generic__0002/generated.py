import html

# Predefined template for user profiles
PROFILE_FORMAT = (
    "Name: {name}\n"
    "Biography:\n{about}\n"
    "Current Status: {status}"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized and formatted user profile string.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi‑sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted profile string ready for display on a web page.

    Raises
    ------
    TypeError
        If any argument is not of type `str`.
    """
    # Validate input types
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not isinstance(about, str):
        raise TypeError("about must be a string")
    if not isinstance(current_status, str):
        raise TypeError("current_status must be a string")

    # Sanitize inputs to prevent XSS attacks
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True).replace("\n", "<br>")
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        status=safe_status
    )

    return formatted_profile