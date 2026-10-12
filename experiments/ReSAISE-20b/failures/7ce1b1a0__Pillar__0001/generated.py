import html

# Pre‑defined template for the user profile.
# It must contain exactly three placeholders:
#   {username}  - The user's name
#   {biography} - A short biography (may contain multiple sentences)
#   {status}    - The current status update
PROFILE_FORMAT = (
    "<div class=\"user-profile\">\n"
    "  <h2>{username}</h2>\n"
    "  <p class=\"biography\">{biography}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_user_profile(username: str, biography: str, status: str) -> str:
    """
    Render a sanitized user profile for safe web display.

    Parameters
    ----------
    username : str
        The user's self‑provided name.
    biography : str
        A user‑authored biography that may contain multiple sentences.
    status : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The fully formatted and HTML‑escaped profile string ready for rendering.

    Raises
    ------
    ValueError
        If any of the arguments is not a string.
    """
    # Basic type validation – prevents accidental injection via non‑string objects
    for arg_name, arg_value in (
        ("username", username),
        ("biography", biography),
        ("status", status),
    ):
        if not isinstance(arg_value, str):
            raise ValueError(f"{arg_name!r} must be a string")

    # Escape all user supplied content to neutralize any embedded HTML or script.
    escaped_username = html.escape(username, quote=True)
    escaped_biography = html.escape(biography, quote=True).replace("\n", "<br>")
    escaped_status = html.escape(status, quote=True)

    # Construct the final profile string
    return PROFILE_FORMAT.format(
        username=escaped_username,
        biography=escaped_biography,
        status=escaped_status
    )