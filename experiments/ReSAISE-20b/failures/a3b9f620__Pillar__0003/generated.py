import html

# Pre‑defined template with placeholders for name, biography and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>\n"
    "  <h1>{name}</h1>\n"
    "  <section class='about-me'>\n"
    "    {bio}\n"
    "  </section>\n"
    "  <footer class='status'>\n"
    "    {status}\n"
    "  </footer>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML representation of a user profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        Sanitized and formatted HTML ready for safe web display.
    """
    # Escape all user‑supplied content to prevent XSS and other injection attacks.
    safe_name = html.escape(full_name, quote=True)
    # Preserve line breaks in the biography by converting newlines to <br> tags.
    safe_bio = html.escape(about_me, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)