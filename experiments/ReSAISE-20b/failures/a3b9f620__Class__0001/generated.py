import html

# Example template: adjust placeholders as needed.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h2>{full_name}</h2>\n"
    "  <p class='about'>About Me: {about_me}</p>\n"
    "  <p class='status'>Status: {status_update}</p>\n"
    "</div>"
)

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Build a safe HTML snippet for a user profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update.

    Returns
    -------
    str
        Sanitized and formatted HTML ready for web display.

    Raises
    ------
    ValueError
        If any argument is not a string or is empty.
    """
    # Basic type and emptiness checks
    for name, value in (
        ("full_name", full_name),
        ("about_me", about_me),
        ("status_update", status_update),
    ):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string.")
        if not value.strip():
            raise ValueError(f"{name} cannot be empty or whitespace only.")

    # Escape user input to neutralize any HTML/JS injection attempts
    safe_full_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Construct the profile using the predefined format
    return PROFILE_FORMAT.format(
        full_name=safe_full_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )