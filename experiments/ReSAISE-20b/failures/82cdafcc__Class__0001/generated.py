import html

# Example template: adjust according to the real web interface.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <div class="status">{status}</div>
</div>
"""

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Build a safe HTML snippet for a user profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        A short current status update.

    Returns
    -------
    str
        Sanitized and formatted HTML ready for display.
    """
    # Sanitize all user‑supplied content to prevent XSS or injection attacks
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Construct the final profile string
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)