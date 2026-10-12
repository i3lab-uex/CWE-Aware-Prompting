import html

# Pre‑defined template for the profile page.
PROFILE_FORMAT = """
<div class="profile">
  <h1>{name}</h1>
  <p class="bio">{bio}</p>
  <div class="status">Status: {status}</div>
</div>
"""

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Render a user profile page from the provided data.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status_message : str
        A brief, current status update from the user.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile information.
    
    Raises
    ------
    ValueError
        If any of the required arguments is empty or consists only of whitespace.
    """
    # Basic validation: ensure all inputs are non‑empty after stripping
    if not fullname or not fullname.strip():
        raise ValueError("fullname must be a non‑empty string")
    if not biography or not biography.strip():
        raise ValueError("biography must be a non‑empty string")
    if not status_message or not status_message.strip():
        raise ValueError("status_message must be a non‑empty string")

    # Escape HTML special characters to prevent XSS attacks
    safe_name = html.escape(fullname.strip())
    safe_bio = html.escape(biography.strip()).replace("\n", "<br>")
    safe_status = html.escape(status_message.strip())

    # Render the template with sanitized values
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status).strip()