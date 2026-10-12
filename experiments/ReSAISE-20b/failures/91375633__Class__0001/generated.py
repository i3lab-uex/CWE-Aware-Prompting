import html

# Template for the user profile.  The placeholders will be replaced with
# escaped values to avoid injection issues.
PROFILE_FORMAT: str = """
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
        The user's display name.
    bio : str
        A potentially multi‑sentence biography.  May contain line breaks.
    status_msg : str
        Short one‑liner status message.

    Returns
    -------
    str
        The HTML string ready for rendering in a web page.  All user input is
        escaped to neutralise special characters that could otherwise break the
        markup or introduce XSS vulnerabilities.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types early
    if not all(isinstance(arg, str) for arg in (name, bio, status_msg)):
        raise TypeError("All arguments must be strings")

    # Escape user input to prevent HTML injection (CWE‑74)
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True).replace("\n", "<br>")
    safe_status = html.escape(status_msg, quote=True)

    # Construct the final profile string
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status
    )