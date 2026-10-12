import html
import re

# Example profile format template.
# It should contain three placeholders: {name}, {bio} and {status}.
PROFILE_FORMAT = """
<div class="profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <div class="status">{status}</div>
</div>
"""

def _sanitize_html(text: str) -> str:
    """
    Escapes HTML special characters to prevent XSS and removes
    any inline script tags that might have slipped through.
    """
    # First escape all HTML characters
    escaped = html.escape(text, quote=True)

    # Remove any remaining <script> tags that were not escaped
    # (unlikely after escaping, but defensive)
    script_re = re.compile(r'<script.*?>.*?</script>', flags=re.IGNORECASE | re.DOTALL)
    cleaned = script_re.sub('', escaped)

    return cleaned

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user profile.

    Parameters
    ----------
    person_name : str
        The user's self-provided name.
    user_bio : str
        A biography that may contain multiple sentences.
    status_message : str
        A short, current status update.

    Returns
    -------
    str
        A sanitized and formatted profile ready for embedding in a web page.

    Raises
    ------
    ValueError
        If any of the inputs are not strings or are empty.
    """
    # Basic type and emptiness checks
    for arg_name, value in (("person_name", person_name),
                            ("user_bio", user_bio),
                            ("status_message", status_message)):
        if not isinstance(value, str):
            raise ValueError(f"{arg_name} must be a string")
        if not value.strip():
            raise ValueError(f"{arg_name} cannot be empty or whitespace")

    # Sanitize each component
    safe_name = _sanitize_html(person_name)
    safe_bio = _sanitize_html(user_bio).replace("\n", "<br>")
    safe_status = _sanitize_html(status_message)

    # Format the profile using the provided template
    return PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)