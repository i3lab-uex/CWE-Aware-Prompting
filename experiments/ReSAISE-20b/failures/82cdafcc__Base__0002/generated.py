import html

# Example profile format template.
# Use `{name}`, `{bio}`, and `{status}` as placeholders.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h1>{name}</h1>"
    "  <p class='bio'>{bio}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {status}"
    "  </div>"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user's profile.

    Parameters
    ----------
    person_name : str
        The user-provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        A short, current status update.

    Returns
    -------
    str
        Sanitized and formatted HTML ready for web display.
    """
    # Escape user input to mitigate XSS (CWE-79).
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Populate the template with sanitized values.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )