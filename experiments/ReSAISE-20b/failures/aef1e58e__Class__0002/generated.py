import html

# Example profile template; in real usage this would be defined elsewhere.
PROFILE_FORMAT = (
    "<div class='profile'>\n"
    "  <h1>{fullname}</h1>\n"
    "  <p class='bio'>{biography}</p>\n"
    "  <footer>{current_status}</footer>\n"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile for web display.

    All user-provided input is HTML-escaped to prevent injection attacks (CWE‑74).
    The function returns a sanitized string that can be safely embedded in an HTML
    document.

    Parameters:
        fullname (str): The user's name.
        biography (str): A multi‑sentence biography written by the user.
        current_status (str): A brief status update.

    Returns:
        str: The formatted, sanitized profile HTML.
    """
    # Escape all user input to neutralize special characters that could alter markup
    safe_fullname = html.escape(fullname, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Insert escaped values into the template
    profile_html = PROFILE_FORMAT.format(
        fullname=safe_fullname,
        biography=safe_biography,
        current_status=safe_status
    )
    return profile_html