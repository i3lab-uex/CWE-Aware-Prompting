import html

# Example template with placeholders for name, bio and status.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <footer>{status}</footer>"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user's profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A potentially multi‑sentence biography authored by the user.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted profile.
    """
    # Sanitize all user input to prevent injection attacks (CWE‑74).
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)