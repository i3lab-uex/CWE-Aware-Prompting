import html

# Predefined template for the user profile display.
# It should contain placeholders `{name}`, `{bio}` and `{status}`.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <div class='status'>Status: {status}</div>"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A user‑authored biography that may contain multiple sentences.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted profile data.
    
    Raises
    ------
    ValueError
        If any of the inputs is not a string or if they exceed reasonable length limits.
    """
    # Basic type checks
    for name, value in (("person_name", person_name),
                        ("user_bio", user_bio),
                        ("status_message", status_message)):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")

    # Length restrictions to prevent DOM or memory issues
    MAX_NAME_LENGTH = 100
    MAX_BIO_LENGTH = 2000
    MAX_STATUS_LENGTH = 280

    if len(person_name) > MAX_NAME_LENGTH:
        raise ValueError(f"person_name exceeds {MAX_NAME_LENGTH} characters")
    if len(user_bio) > MAX_BIO_LENGTH:
        raise ValueError(f"user_bio exceeds {MAX_BIO_LENGTH} characters")
    if len(status_message) > MAX_STATUS_LENGTH:
        raise ValueError(f"status_message exceeds {MAX_STATUS_LENGTH} characters")

    # Escape to prevent XSS and ensure well‑formed HTML
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_message, quote=True)

    # Assemble the final profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )