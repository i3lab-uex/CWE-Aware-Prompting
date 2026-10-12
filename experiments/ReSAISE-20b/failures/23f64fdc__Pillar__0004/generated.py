import html

# Predefined template with placeholders for name, biography and status
PROFILE_FORMAT = """
<div class="user-profile">
    <h1>{name}</h1>
    <p class="biography">{bio}</p>
    <div class="status">{status}</div>
</div>
"""

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user‑written biography (may contain multiple sentences).
    status : str
        The user's current brief status message.

    Returns
    -------
    str
        A fully escaped HTML string ready for inclusion in a web page.

    Raises
    ------
    ValueError
        If any of the required placeholders are missing from PROFILE_FORMAT.
    """
    # Validate that all placeholders exist in the template
    required_keys = {"name", "bio", "status"}
    missing = required_keys - set(PROFILE_FORMAT.format_map(lambda k: k).keys())
    if missing:
        raise ValueError(f"Missing placeholders in PROFILE_FORMAT: {missing}")

    # Escape user input to prevent XSS (CWE-707 mitigation)
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the template with sanitized values
    rendered_profile = PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)
    return rendered_profile