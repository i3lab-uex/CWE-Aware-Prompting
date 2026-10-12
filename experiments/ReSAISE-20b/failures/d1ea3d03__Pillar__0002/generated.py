import html

# Predefined profile format template.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Render a user profile page safely by escaping user-provided content.

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
        The sanitized and formatted HTML string for the profile page.
    """
    # Escape all user-supplied content to avoid XSS and ensure proper
    # formatting of the output. The `html.escape` function converts
    # special characters to their HTML entity equivalents.
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