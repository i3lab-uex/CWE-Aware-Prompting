import html

# Example template with placeholders for name, biography and status.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="biography">{bio}</p>
  <div class="status">{status}</div>
</div>
"""

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Build a safe HTML snippet for displaying a user's profile.

    Parameters
    ----------
    username : str
        The user-provided name.
    biography : str
        A potentially multi‑sentence bio written by the user.
    status : str
        The user's current short status message.

    Returns
    -------
    str
        An HTML string with all user input properly escaped to prevent
        cross‑site scripting (XSS) or other injection attacks.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate input types to avoid accidental injection via non‑string objects
    if not all(isinstance(arg, str) for arg in (username, biography, status)):
        raise TypeError("All arguments must be of type str")

    # Escape user input to neutralize special HTML characters
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the provided template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)