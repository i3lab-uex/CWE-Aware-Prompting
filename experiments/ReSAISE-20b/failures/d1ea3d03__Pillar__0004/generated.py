import html

# Pre‑defined template string for user profiles.
# It contains named placeholders that will be replaced by the function.
PROFILE_FORMAT: str = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status}\n"
    "  </div>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML snippet for a user's profile page.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted profile information.
    """
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape all user supplied content to prevent XSS and other injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template.
    rendered = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return rendered