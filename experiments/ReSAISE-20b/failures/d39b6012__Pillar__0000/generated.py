import html

# Predefined profile template with placeholders for name, bio and status.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <div class="status">{status}</div>
</div>
"""

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile string.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The sanitized and formatted HTML snippet representing the user's profile.
    """
    # Basic validation: ensure inputs are strings
    if not all(isinstance(arg, str) for arg in (user_name, biography, status)):
        raise TypeError("All arguments must be strings")

    # Escape HTML special characters to prevent injection attacks.
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status, quote=True)

    # Construct the final profile using the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)