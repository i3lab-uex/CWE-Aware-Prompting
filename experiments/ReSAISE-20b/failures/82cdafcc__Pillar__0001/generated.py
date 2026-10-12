import html

# Example template; adjust placeholders as needed for your UI framework.
PROFILE_FORMAT = """
<div class="user-profile">
  <h2>{name}</h2>
  <p class="bio">{bio}</p>
  <div class="status">{status}</div>
</div>
"""

def display_user_profile(person_name: str, user_bio: str, status_message: str) -> str:
    """
    Construct a safe HTML snippet for displaying a user's profile.

    Parameters
    ----------
    person_name : str
        The user's self‑provided name.
    user_bio : str
        A biography written by the user. May contain multiple sentences.
    status_message : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string containing the sanitized profile data, ready for rendering.

    Raises
    ------
    ValueError
        If any input is not a string or exceeds a reasonable length (CWE‑707 mitigation).
    """
    # Basic type checks
    for name, val in (("person_name", person_name), ("user_bio", user_bio),
                      ("status_message", status_message)):
        if not isinstance(val, str):
            raise ValueError(f"{name} must be a string")

    # Length limits to avoid denial‑of‑service or oversized payloads
    MAX_NAME_LEN = 100
    MAX_BIO_LEN = 2000
    MAX_STATUS_LEN = 280

    if len(person_name) > MAX_NAME_LEN:
        raise ValueError(f"person_name exceeds {MAX_NAME_LEN} characters")
    if len(user_bio) > MAX_BIO_LEN:
        raise ValueError(f"user_bio exceeds {MAX_BIO_LEN} characters")
    if len(status_message) > MAX_STATUS_LEN:
        raise ValueError(f"status_message exceeds {MAX_STATUS_LEN} characters")

    # Escape all user supplied content to neutralize HTML injection
    safe_name = html.escape(person_name, quote=True)
    safe_bio = html.escape(user_bio, quote=False)  # quotes not required in <p>
    safe_status = html.escape(status_message, quote=True)

    # Format the profile using a pre‑defined template
    rendered = PROFILE_FORMAT.format(name=safe_name, bio=safe_bio, status=safe_status)
    return rendered