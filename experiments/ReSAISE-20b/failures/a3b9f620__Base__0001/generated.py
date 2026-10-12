import html

# Example template (this would normally be defined elsewhere in your codebase)
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h1>{name}</h1>"
    "  <p class='about'>About me: {about}</p>"
    "  <p class='status'>Status: {status}</p>"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user's profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences and HTML special characters.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted profile ready for inclusion in a web page.

    Notes
    -----
    All user input is escaped using `html.escape` to prevent Cross‑Site Scripting (XSS)
    attacks. No further sanitization is performed because the template does not
    allow arbitrary HTML tags or attributes.
    """
    # Escape user input to neutralize potentially malicious content
    safe_name = html.escape(full_name, quote=True)
    safe_about = html.escape(about_me, quote=True)
    safe_status = html.escape(status_update, quote=True)

    # Format the profile using the provided template
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        status=safe_status
    )