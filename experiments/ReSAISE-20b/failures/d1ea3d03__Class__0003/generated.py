import html

# Pre‑defined template string for formatting user profiles.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized and formatted user profile HTML snippet.

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
        The sanitized and formatted HTML string ready for inclusion in a web page.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or are empty.
    """
    # Basic type and emptiness checks
    if not all(isinstance(arg, str) for arg in (fullname, biography, status_message)):
        raise ValueError("All arguments must be strings.")
    if not fullname.strip() or not biography.strip() or not status_message.strip():
        raise ValueError("Arguments must contain non‑empty content.")

    # Escape all user input to prevent HTML injection (CWE-74)
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )