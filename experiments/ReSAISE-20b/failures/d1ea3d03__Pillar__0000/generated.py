import html

# Pre‑defined template for the profile page.
PROFILE_FORMAT = (
    "<div class=\"profile\">\n"
    "  <h1>{name}</h1>\n"
    "  <p class=\"bio\">{bio}</p>\n"
    "  <footer>{status}</footer>\n"
    "</div>"
)

def render_profile_page(fullname: str, biography: str, status_message: str) -> str:
    """
    Generate a sanitized and formatted user profile page.

    Args:
        fullname: The user's full name.
        biography: A multi‑sentence biography provided by the user.
        status_message: A brief, current status update from the user.

    Returns:
        A string containing the sanitized and formatted profile information
        ready to be embedded in an HTML page.

    Raises:
        TypeError: If any argument is not a string.
        ValueError: If any argument is an empty string after stripping whitespace.
    """
    # Validate input types
    for arg_name, value in (
        ("fullname", fullname),
        ("biography", biography),
        ("status_message", status_message),
    ):
        if not isinstance(value, str):
            raise TypeError(f"{arg_name} must be a string, got {type(value).__name__}")

    # Trim whitespace and check for emptiness
    if not fullname.strip():
        raise ValueError("fullname cannot be empty or whitespace only")
    if not biography.strip():
        raise ValueError("biography cannot be empty or whitespace only")
    if not status_message.strip():
        raise ValueError("status_message cannot be empty or whitespace only")

    # Escape user‑supplied content to prevent XSS
    safe_name = html.escape(fullname.strip(), quote=True)
    safe_bio = html.escape(biography.strip(), quote=True)
    safe_status = html.escape(status_message.strip(), quote=True)

    # Render the profile using the predefined template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)