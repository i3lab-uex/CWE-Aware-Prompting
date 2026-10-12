import html

# Pre‑defined template with placeholders for name, bio and status message.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer>{status_message}</footer>\n"
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
        A multi‑sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted profile HTML string.

    Raises
    ------
    ValueError
        If any of the arguments are missing or not strings.
    """
    # Basic type checking
    if not all(isinstance(arg, str) for arg in (fullname, biography, status_message)):
        raise ValueError("All arguments must be strings")

    # Escape HTML special characters to avoid XSS
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=False).replace("\n", "<br>")
    safe_status = html.escape(status_message, quote=True)

    # Format using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status_message=safe_status
    )