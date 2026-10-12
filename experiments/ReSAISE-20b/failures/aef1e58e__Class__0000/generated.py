import html

# Predefined template for rendering a user profile.
PROFILE_FORMAT = (
    "<div class='profile'>"
    "  <h1>{name}</h1>"
    "  <p class='bio'>{biography}</p>"
    "  <footer>{status}</footer>"
    "</div>"
)

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user profile for web display.

    The function sanitizes all input strings to prevent HTML injection
    (CWE-74) by escaping special characters. The sanitized values are then
    inserted into a predefined HTML template.

    Parameters:
        fullname (str): The user's full name.
        biography (str): A potentially multi‑sentence biography.
        current_status (str): A short status update.

    Returns:
        str: The fully formatted, sanitized HTML profile.
    """
    # Escape user input to neutralize special characters that could break
    # the HTML structure or inject malicious content.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Render the template with sanitized values
    return PROFILE_FORMAT.format(
        name=safe_name,
        biography=safe_bio,
        status=safe_status
    )