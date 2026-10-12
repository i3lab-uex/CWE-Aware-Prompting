import html

# Example template; in real usage this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{biography}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    username : str
        The user's self‑provided name.
    biography : str
        A potentially multi‑sentence biography authored by the user.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The sanitized and formatted HTML string ready for safe web display.

    Raises
    ------
    ValueError
        If the template does not contain all required placeholders.
    """
    # Ensure the template contains the expected placeholders
    for placeholder in ("{name}", "{biography}", "{status}"):
        if placeholder not in PROFILE_FORMAT:
            raise ValueError(f"Template missing required placeholder: {placeholder}")

    # Escape user‑supplied content to prevent HTML/JS injection
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the sanitized values
    return PROFILE_FORMAT.format(name=safe_name, biography=safe_bio, status=safe_status)