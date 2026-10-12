import html

# Predefined template for rendering a user profile.
# It uses Python format placeholders that will be replaced with the sanitized values.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <div class='status'>\n"
    "    <strong>Status:</strong> {status_message}\n"
    "  </div>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML representation of a user's profile.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted profile HTML string.
    """
    # Sanitize all user-provided inputs to prevent XSS attacks (CWE-79).
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status_message = html.escape(status_message, quote=True)

    # Format the profile using the pre-defined template.
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        status_message=safe_status_message
    )