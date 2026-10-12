import html

# Pre‑defined template string for formatting user profiles.
# It uses Python format placeholders: {name}, {bio}, {status}
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer class=\"status\">{status}</footer>\n"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized and formatted user profile HTML snippet.

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
        A string containing the sanitized and formatted user profile information.
    
    Notes
    -----
    All user input is escaped using html.escape to prevent HTML injection (CWE‑74).
    """
    # Sanitize user inputs by escaping special HTML characters.
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template.
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )
    return formatted_profile