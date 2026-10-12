import html

# Predefined template for user profiles.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <footer class="status">Status: {status}</footer>
</div>
"""

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML user profile from the provided data.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi-sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        Sanitized and formatted HTML string ready for rendering on a web page.

    Raises
    ------
    ValueError
        If any of the arguments is not a string or is empty after stripping.
    """
    # Basic type checks
    for name, value in (("user_name", user_name), ("biography", biography), ("status", status)):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")

    # Trim whitespace and ensure non-empty
    user_name = user_name.strip()
    biography = biography.strip()
    status = status.strip()

    if not user_name or not biography or not status:
        raise ValueError("All fields must contain non-empty values")

    # Sanitize inputs to prevent XSS and ensure proper HTML structure
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Render the profile using the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)