import html

# Predefined template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{fullname}</h2>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <div class=\"status\">{current_status}</div>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    fullname : str
        The user's name as entered.
    biography : str
        A potentially multi‑sentence user biography.
    current_status : str
        The user's brief, current status message.

    Returns
    -------
    str
        A string containing the profile HTML with all user input safely escaped.

    Notes
    -----
    All inputs are passed through html.escape to neutralize any characters that could be
    interpreted as HTML or JavaScript, mitigating CWE‑74 (Improper Neutralization of Special Elements in Output).
    """
    # Escape all user input to prevent injection.
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the sanitized values.
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )