import html

# Pre‑defined template for the profile display.  The placeholders will be
# replaced with sanitized values.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{full_name}</h2>\n"
    "  <p class='about'>{about_me}</p>\n"
    "  <div class='status'>Status: {status_update}</div>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML snippet containing the user's profile.

    Parameters
    ----------
    full_name : str
        The user‑supplied name.
    about_me : str
        A multi‑sentence biography written by the user.
    status_update : str
        The current status message.

    Returns
    -------
    str
        An HTML fragment with all user input properly escaped to prevent
        injection attacks (CWE‑74).
    """
    # Escape all user input so that no markup or script can be injected.
    safe_name = html.escape(full_name, quote=True)
    safe_about = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the pre‑defined template.
    return PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_about,
        status_update=safe_status
    )