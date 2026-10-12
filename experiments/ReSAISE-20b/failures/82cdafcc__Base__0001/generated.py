import html

# Example template; in a real application this would be imported or defined elsewhere.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "<h1>{name}</h1>"
    "<p class='bio'>{bio}</p>"
    "<footer class='status'>Status: {status}</footer>"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized HTML snippet for displaying a user's profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        A short, current status update.

    Returns
    -------
    str
        An HTML string ready for safe rendering on a web page.

    Raises
    ------
    ValueError
        If any argument is not a string.
    """
    # Basic type checks
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise ValueError("All arguments must be strings.")

    # Escape all user supplied content to mitigate XSS (CWE‑79)
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the provided template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile