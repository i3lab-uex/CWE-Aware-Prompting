import html

# Pre‑defined template for rendering a user profile on the web page.
PROFILE_FORMAT: str = (
    "<div class='user-profile'>"
    "  <h2>{name}</h2>"
    "  <p class='bio'>{about}</p>"
    "  <div class='status'>"
    "    <strong>Status:</strong> {current_status}"
    "  </div>"
    "</div>"
)

def display_user_profile(username: str, about: str, current_status: str) -> str:
    """
    Generate a sanitized HTML snippet that displays a user's profile.

    Parameters
    ----------
    username : str
        The full name of the user.
    about : str
        A multi‑sentence biography supplied by the user.
    current_status : str
        A brief, current status update from the user.

    Returns
    -------
    str
        An HTML string with the user's profile safely escaped to prevent
        injection attacks such as XSS or HTML injection.

    Raises
    ------
    ValueError
        If any of the arguments is not a string or is empty.
    """
    # Validate input types and non‑emptiness
    for arg_name, arg_value in (
        ("username", username),
        ("about", about),
        ("current_status", current_status),
    ):
        if not isinstance(arg_value, str):
            raise ValueError(f"{arg_name} must be a string")
        if not arg_value.strip():
            raise ValueError(f"{arg_name} must not be empty")

    # Escape user input to neutralise special HTML characters
    safe_name = html.escape(username, quote=True)
    safe_about = html.escape(about, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Render the profile using the sanitized values
    return PROFILE_FORMAT.format(
        name=safe_name,
        about=safe_about,
        current_status=safe_status,
    )