import html

# Template for displaying user profiles.
# Placeholders: {name}, {bio}, {status_msg}
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{name}</h2>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer>{status_msg}</footer>\n"
    "</div>"
)

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Sanitize user-provided data and format it for display on a webpage.

    Parameters
    ----------
    name : str
        The user's name.
    bio : str
        The user's biography (may contain multiple sentences).
    status_msg : str
        A short status message or one-liner from the user.

    Returns
    -------
    str
        A concatenated, sanitized HTML snippet ready for rendering.
    """
    # Ensure inputs are strings and escape special HTML characters
    safe_name = html.escape(str(name))
    safe_bio = html.escape(str(bio))
    safe_status_msg = html.escape(str(status_msg))

    # Format the profile using the predefined template
    formatted_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )

    return formatted_profile