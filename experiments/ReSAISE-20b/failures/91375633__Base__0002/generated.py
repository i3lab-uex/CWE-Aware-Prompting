import html

# Template for the user profile HTML.
PROFILE_FORMAT: str = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <footer class="status">{status_msg}</footer>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Safely format and return a user profile for display on a webpage.

    Parameters
    ----------
    name : str
        The user's full name.
    bio : str
        A short biography; may contain multiple sentences and HTML‑like characters.
    status_msg : str
        A one‑liner status update from the user.

    Returns
    -------
    str
        The HTML snippet containing the escaped values inserted into PROFILE_FORMAT.
    """
    # Escape user‑controlled input to prevent XSS (CWE‑79).
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )