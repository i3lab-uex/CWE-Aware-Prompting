import html

# Pre‑defined template with placeholders for name, biography and status.
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{username}</h2>"
    "  <p class='bio'>{biography}</p>"
    "  <div class='status'>Status: {status}</div>"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for safe web display.

    Parameters
    ----------
    username : str
        The user's self‑provided name.
    biography : str
        A user‑authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile ready for
        safe web display.

    Raises
    ------
    ValueError
        If any of the required placeholders are missing from PROFILE_FORMAT.
    """
    # Verify that all placeholders exist in the template
    required_keys = {"username", "biography", "status"}
    missing = required_keys - PROFILE_FORMAT.format_map(
        {k: "" for k in required_keys}
    ).keys()
    if missing:
        raise ValueError(f"Missing placeholders in PROFILE_FORMAT: {missing}")

    # Escape all user input to prevent XSS and other injection attacks
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the sanitized inputs
    rendered_profile = PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )

    return rendered_profile