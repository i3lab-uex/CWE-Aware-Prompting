import html

# Predefined template for the user profile display.
PROFILE_FORMAT = """
<div class="user-profile">
  <h1>{username}</h1>
  <p class="biography">{biography}</p>
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
        A user‑written biography that may span multiple sentences.
    status : str
        A brief, current status message provided by the user.

    Returns
    -------
    str
        The profile string with all user input safely escaped for HTML.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Basic type checking to avoid unexpected errors
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be of type str.")

    # Escape user input to neutralize potential XSS payloads
    safe_username = html.escape(username, quote=True)
    safe_biography = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(
        username=safe_username,
        biography=safe_biography,
        status=safe_status
    )