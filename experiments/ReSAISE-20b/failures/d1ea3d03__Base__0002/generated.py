import html

# A simple template for rendering a user profile. The placeholders are used with str.format.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Render a sanitized user profile page.

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
        An HTML string containing the sanitized and formatted profile information.
    """
    # Sanitize all user-controlled input to prevent XSS (CWE-79).
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