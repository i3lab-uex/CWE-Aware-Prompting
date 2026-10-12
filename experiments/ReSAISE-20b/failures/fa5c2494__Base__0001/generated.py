import html

# Pre‑defined template for the user profile.  The placeholders will be replaced by
# the sanitized values of username, about and current_status.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a safe HTML snippet that displays a user profile.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi‑sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string containing the sanitized and formatted user profile.
    """
    # Escape all user‑provided input to prevent XSS attacks (CWE‑79).
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the template.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)