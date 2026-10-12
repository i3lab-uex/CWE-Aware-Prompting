import html

# Pre‑defined template for the profile display.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <div class="status">Status: {status}</div>
</div>
"""

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Build a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The profile HTML with all user input safely escaped.
    
    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Ensure all arguments are strings
    if not isinstance(full_name, str):
        raise TypeError(f"full_name must be a string, got {type(full_name).__name__}")
    if not isinstance(about_me, str):
        raise TypeError(f"about_me must be a string, got {type(about_me).__name__}")
    if not isinstance(status_update, str):
        raise TypeError(f"status_update must be a string, got {type(status_update).__name__}")

    # Escape user input to prevent XSS
    safe_name = html.escape(full_name, quote=True)
    safe_bio = html.escape(about_me, quote=False).replace("\n", "<br>")
    safe_status = html.escape(status_update, quote=True)

    # Populate the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)