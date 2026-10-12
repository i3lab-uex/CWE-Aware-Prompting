import html

# Example template – adjust as needed for your web framework.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{biography}</p>
  <div class="status">{status}</div>
</div>
"""

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user profile for web display.

    Parameters
    ----------
    fullname : str
        The user's full name as entered.
    biography : str
        A user‑written bio that may contain multiple sentences.
    current_status : str
        A brief status message.

    Returns
    -------
    str
        A sanitized, formatted HTML snippet ready for injection into a page.
    """
    # Sanitize all user input to prevent XSS or other injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Construct the final profile string using the template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )