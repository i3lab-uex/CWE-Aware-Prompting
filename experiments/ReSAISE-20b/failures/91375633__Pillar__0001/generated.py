import html

# Template for the user profile display.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{name}</h2>
    <p class="bio">{bio}</p>
    <footer class="status">{status_msg}</footer>
</div>
"""

def show_user_profile(name: str, bio: str, status_msg: str) -> str:
    """
    Sanitize user-provided data and return an HTML snippet
    that displays a user profile.

    Parameters:
        name (str): The user's name.
        bio (str): The user's biography, may contain multiple sentences.
        status_msg (str): A short status message or one-liner from the user.

    Returns:
        str: A safe, concatenated HTML string ready for rendering.
    """
    # Escape all user-supplied content to prevent XSS and other injection attacks
    safe_name = html.escape(name, quote=True)
    safe_bio = html.escape(bio, quote=True)
    safe_status_msg = html.escape(status_msg, quote=True)

    # Format the profile using the template
    rendered_profile = PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status_msg=safe_status_msg
    )

    return rendered_profile.strip()