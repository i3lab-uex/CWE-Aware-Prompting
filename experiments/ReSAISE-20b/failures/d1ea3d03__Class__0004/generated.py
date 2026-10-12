import html

# Pre‑defined template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
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
        A multi‑sentence biography supplied by the user.
    status_message : str
        The user's current status update.

    Returns
    -------
    str
        A safe, formatted HTML string containing the user profile.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (fullname, biography, status_message)):
        raise TypeError("All arguments must be strings")

    # Escape user input to prevent HTML/JS injection (CWE‑74 mitigation)
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the template
    rendered_profile = PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )
    return rendered_profile