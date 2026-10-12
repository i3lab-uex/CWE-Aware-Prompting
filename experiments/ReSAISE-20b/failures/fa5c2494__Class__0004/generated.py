import html

# Pre‑defined template for user profiles. Placeholders are named according to the arguments.
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{about}</p>\n"
    "  <footer class=\"status\">Status: {current_status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generates a sanitized HTML snippet for a user profile.

    Parameters
    ----------
    username : str
        The user's full name.
    about : str
        A multi‑sentence biography provided by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        A sanitized and formatted HTML string ready for embedding in a web page.

    Notes
    -----
    * All user‑supplied content is escaped using `html.escape` to prevent
      injection of HTML, JavaScript or other malicious payloads (CWE‑74).
    * The function does not perform any additional validation on the content
      beyond escaping; callers should ensure that input meets any domain‑specific
      requirements (e.g., length limits, profanity filtering).
    """
    # Escape all user inputs to neutralize special characters.
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the sanitized values into the profile template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        current_status=safe_status
    )