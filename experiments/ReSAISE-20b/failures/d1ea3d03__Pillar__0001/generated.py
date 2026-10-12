import html

# Pre‑defined format template for a user profile page.
# The placeholders are named to be clear and explicit.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
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
        A multi‑sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The HTML string containing the sanitized and formatted profile.
    """
    # Basic type checking for safety
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a string")
    if not isinstance(biography, str):
        raise TypeError("biography must be a string")
    if not isinstance(status_message, str):
        raise TypeError("status_message must be a string")

    # Escape all user input to prevent XSS and other injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Render the profile using the pre‑defined format.
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )