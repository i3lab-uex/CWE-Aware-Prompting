import html

# Template for rendering a user profile.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <footer class="status">{status_msg}</footer>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Return a sanitized HTML snippet containing the user's profile.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        A potentially multi‑sentence biography. May contain user supplied text.
    status_msg : str
        Short one‑liner status message from the user.

    Returns
    -------
    str
        A safe, sanitized HTML string ready for embedding in a page.

    Raises
    ------
    TypeError
        If any argument is not of type `str`.
    """
    # Validate input types.
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not isinstance(bio, str):
        raise TypeError("bio must be a string")
    if not isinstance(status_msg, str):
        raise TypeError("status_msg must be a string")

    # Escape user supplied data to avoid XSS.
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_msg, quote=True)

    # Format the profile using the template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )