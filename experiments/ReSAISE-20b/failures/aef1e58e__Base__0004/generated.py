import html

# Predefined template for rendering the profile on a web page.
# Placeholders: {fullname}, {biography}, {current_status}
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{fullname}</h2>
    <p class="biography">{biography}</p>
    <div class="status">Status: {current_status}</div>
</div>
"""

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user profile for web display.

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
        A sanitized HTML snippet containing the profile information.

    Raises
    ------
    ValueError
        If any argument is not a string or is empty after stripping.
    """
    # Basic validation
    for name, value in (("fullname", fullname), ("biography", biography),
                        ("current_status", current_status)):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")
        if not value.strip():
            raise ValueError(f"{name} cannot be empty")

    # Escape user input to prevent XSS (CWE‑79)
    escaped_fullname = html.escape(fullname, quote=True)
    escaped_biography = html.escape(biography, quote=True)
    escaped_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        fullname=escaped_fullname,
        biography=escaped_biography,
        current_status=escaped_status
    )