import html

# Template for the user profile; placeholders are marked with {name}, {bio} and {status}
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
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
        A user‑written biography that may span multiple sentences.
    status : str
        The user's current status message.

    Returns
    -------
    str
        A formatted string containing the sanitized user profile ready for rendering in HTML.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise ValueError("All arguments must be strings")

    # Escape any special HTML characters to prevent injection attacks
    safe_name = html.escape(username.strip())
    safe_bio = html.escape(biography.strip())
    safe_status = html.escape(status.strip())

    # Render the template with sanitized values
    rendered_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )

    return rendered_profile.strip()