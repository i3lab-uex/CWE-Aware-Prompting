import html

# Example profile format template.
# Replace with the actual format used in your application.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <div class=\"status\">{status}</div>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Construct a sanitized HTML snippet for displaying a user profile.

    Parameters
    ----------
    username : str
        The user's self-provided name.
    biography : str
        A user-authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        A sanitized and formatted HTML string ready for safe web display.

    Raises
    ------
    ValueError
        If any of the required placeholders are missing from PROFILE_FORMAT.
    """
    # Ensure that the template contains all required placeholders
    required_placeholders = {"username", "biography", "status"}
    missing = required_placeholders - set(PROFILE_FORMAT.format_map({k: "" for k in required_placeholders}).keys())
    if missing:
        raise ValueError(f"PROFILE_FORMAT is missing placeholders: {missing}")

    # Escape user input to prevent injection (CWE-74)
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Build the final HTML
    rendered = PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )
    return rendered