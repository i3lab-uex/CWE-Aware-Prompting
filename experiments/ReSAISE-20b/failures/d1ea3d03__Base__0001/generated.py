import html

# Predefined template for the profile page.  It uses named placeholders.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Render a user profile page safely.

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
        The sanitized and formatted profile HTML.
    """
    # Escape all user-provided input to prevent XSS attacks (CWE-79).
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the pre-defined template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )