import html

# Pre‑defined template for user profiles.
# Placeholders: {name}, {bio}, {status}
PROFILE_FORMAT = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{bio}</p>"
    "  <footer><em>{status}</em></footer>"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized and formatted user profile string.

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
        The sanitized and formatted HTML string ready for display.
    """
    # Escape user input to prevent XSS attacks (CWE-707).
    safe_name = html.escape(username, quote=True)
    safe_bio = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template.
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )