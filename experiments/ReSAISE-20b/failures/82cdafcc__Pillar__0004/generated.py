import html

# Example template for the user profile display.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a sanitized and formatted user profile for web display.

    Parameters
    ----------
    person_name : str
        The user's self-provided name.
    user_bio : str
        A user-authored biography that may contain multiple sentences.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted HTML snippet ready for safe display.
    """
    # Sanitize all user-supplied inputs to prevent XSS and ensure well‑formed HTML.
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Use the predefined template to assemble the final output.
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return formatted_profile