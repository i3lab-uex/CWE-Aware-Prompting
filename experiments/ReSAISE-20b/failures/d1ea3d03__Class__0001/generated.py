import html

# Predefined template for the profile page.
PROFILE_FORMAT = """
<div class="profile">
    <h1>{name}</h1>
    <p class="bio">{bio}</p>
    <footer class="status">{status}</footer>
</div>
"""

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized HTML profile page from user-provided data.

    Parameters
    ----------
    fullname : str
        The user's full name.
    biography : str
        A multi‑sentence biography supplied by the user.
    status_message : str
        The user's current status update.

    Returns
    -------
    str
        A string containing the sanitized and formatted user profile.
    """
    # Escape all user input to prevent HTML/JS injection (CWE‑74).
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_message, quote=True)

    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)