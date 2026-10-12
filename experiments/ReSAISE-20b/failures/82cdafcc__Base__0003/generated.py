import html

# Example template; in a real application this would be defined elsewhere.
PROFILE_FORMAT = """
<div class="profile">
    <h1>{name}</h1>
    <p class="bio">{bio}</p>
    <footer><em>{status}</em></footer>
</div>
"""

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML profile snippet for display.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        The current status update.

    Returns
    -------
    str
        A sanitized and formatted HTML snippet ready for web rendering.

    Raises
    ------
    TypeError
        If any argument is not a string.
    """
    # Validate types to avoid accidental injection of non‑string objects
    if not all(isinstance(arg, str) for arg in (person_name, user_bio, status_message)):
        raise TypeError("All arguments must be strings")

    # Escape user input to neutralize potential XSS vectors
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=True)
    safe_status = html.escape(status_message, quote=True)

    # Build the final HTML using a predefined template
    profile_html = PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)
    return profile_html