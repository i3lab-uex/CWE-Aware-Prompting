import html

# Template for the user profile. The placeholders are marked with {name}, {bio}, and {status}.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <div class="status">{status}</div>
</div>
"""

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized HTML snippet for a user profile.

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
        An HTML string containing the sanitized and formatted user profile information.

    Raises
    ------
    ValueError
        If any of the arguments are not strings.
    """
    # Validate input types
    if not isinstance(user_name, str):
        raise ValueError("user_name must be a string")
    if not isinstance(biography, str):
        raise ValueError("biography must be a string")
    if not isinstance(status, str):
        raise ValueError("status must be a string")

    # Escape all user-provided content to prevent XSS
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status, quote=True)

    # Format the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)