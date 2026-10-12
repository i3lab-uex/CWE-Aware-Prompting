import html

# Pre‑defined template for user profiles.
# The placeholders {name}, {bio} and {status} will be replaced with
# sanitized user input.  The format is intentionally simple to avoid
# accidental parsing errors (CWE‑707).
PROFILE_FORMAT: str = (
    "User Profile\n"
    "------------\n"
    "Name   : {name}\n"
    "Bio    : {bio}\n"
    "Status : {status}"
)

def create_user_profile(user_name: str, biography: str, status: str) -> str:
    """
    Generate a sanitized and formatted user profile string.

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
        The profile string with all fields escaped to prevent HTML or
        script injection.  The output is guaranteed to be well‑formed
        according to the PROFILE_FORMAT template.

    Raises
    ------
    ValueError
        If any of the arguments is not a string or if they are empty.
    """
    # Validate input types and non‑emptiness
    for arg_name, value in (("user_name", user_name), ("biography", biography), ("status", status)):
        if not isinstance(value, str):
            raise ValueError(f"{arg_name} must be a string")
        if not value.strip():
            raise ValueError(f"{arg_name} cannot be empty or whitespace only")

    # Escape user input to neutralise potential markup/script injection
    safe_name = html.escape(user_name, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(status, quote=True)

    # Construct the profile using the template
    return PROFILE_FORMAT.format(
        name=safe_name,
        bio=safe_bio,
        status=safe_status
    )