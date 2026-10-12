import html

# Pre‑defined template for rendering a user profile on the web page.
# The placeholders `{name}`, `{bio}` and `{status}` will be substituted
# with the user‑provided data after sanitisation.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>\n"
    "  <h2>{name}</h2>\n"
    "  <p class='bio'>{bio}</p>\n"
    "  <footer><em>{status}</em></footer>\n"
    "</div>"
)


def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile for display on a web page.

    Parameters
    ----------
    user_name : str
        The user's full name.
    biography : str
        A multi‑sentence biography provided by the user.
    status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        The HTML snippet containing the sanitized profile information.

    Raises
    ------
    ValueError
        If any of the required arguments are empty or not strings.
    """
    # Basic type and emptiness checks
    for arg_name, value in (("user_name", user_name),
                            ("biography", biography),
                            ("status", status)):
        if not isinstance(value, str):
            raise ValueError(f"Argument '{arg_name}' must be a string.")
        if not value.strip():
            raise ValueError(f"Argument '{arg_name}' cannot be empty or whitespace.")

    # Escape user input to prevent XSS attacks
    safe_name = html.escape(user_name.strip())
    safe_bio = html.escape(biography.strip()).replace("\n", "<br>")
    safe_status = html.escape(status.strip())

    # Render the profile using the template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)