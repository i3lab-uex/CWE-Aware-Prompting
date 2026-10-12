import html

# Predefined format string for the user profile.
# Example: "Name: {username}\nBio: {biography}\nStatus: {status}"
PROFILE_FORMAT = (
    "Name: {username}\n"
    "Biography:\n{biography}\n\n"
    "Current Status:\n{status}"
)

def generate_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for web display.

    Parameters
    ----------
    username : str
        The user's name as entered.
    biography : str
        A user-written biography, possibly spanning multiple sentences.
    status : str
        A brief, current status message.

    Returns
    -------
    str
        The formatted profile string with all user-supplied content safely escaped.

    Notes
    -----
    - All user input is passed through `html.escape` to neutralize HTML
      special characters, mitigating XSS (CWE-79) and preventing malformed
      markup that could break the surrounding page.
    - The function uses a predefined format string containing placeholders
      for the three fields; no dynamic code execution or eval is involved.
    """
    # Escape all user-supplied data to avoid injection issues
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status, quote=True)

    # Render the profile using the format string
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )