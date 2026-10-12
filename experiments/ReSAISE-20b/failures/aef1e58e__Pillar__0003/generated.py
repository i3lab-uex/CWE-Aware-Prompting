import html

# Example template – replace with the actual format used in your application.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <footer>{current_status}</footer>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    fullname : str
        The user's full name as entered.
    biography : str
        A user-provided biography, possibly multi‑sentence.
    current_status : str
        The user's brief current status message.

    Returns
    -------
    str
        A string containing the profile HTML with all user input safely escaped.

    Raises
    ------
    TypeError
        If any argument is not a string.
    ValueError
        If the template does not contain all required placeholders.
    """
    # Validate argument types
    for name, value in (("fullname", fullname),
                        ("biography", biography),
                        ("current_status", current_status)):
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string, got {type(value).__name__}")

    # Escape user input to prevent XSS or injection attacks
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Ensure the template contains all required placeholders
    missing = {ph for ph in ("fullname", "biography", "current_status") if f"{{{ph}}}" not in PROFILE_FORMAT}
    if missing:
        raise ValueError(f"PROFILE_FORMAT is missing placeholders: {', '.join(missing)}")

    # Format the profile safely
    return PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )