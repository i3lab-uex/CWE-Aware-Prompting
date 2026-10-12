import html

# Assume PROFILE_FORMAT is defined elsewhere in the application.
# Example:
# PROFILE_FORMAT = "<h1>{name}</h1><p>{bio}</p><blockquote>{status}</blockquote>"
# The function uses the placeholders 'name', 'bio', and 'status'.

def display_user_profile(fullname: str, biography: str, current_status: str) -> str:
    """
    Render a user's profile for web display.

    Parameters
    ----------
    fullname : str
        The user's full name as entered.
    biography : str
        A user-provided biography that may contain multiple sentences.
    current_status : str
        The user's current status message.

    Returns
    -------
    str
        A formatted string with the sanitized profile information.
    """
    # Sanitize each user input to prevent XSS and other injection attacks.
    safe_name = html.escape(fullname, quote=True)
    safe_bio = html.escape(biography, quote=True)
    safe_status = html.escape(current_status, quote=True)

    # Format the profile using the predefined template.
    try:
        formatted_profile = PROFILE_FORMAT.format(
            name=safe_name,
            bio=safe_bio,
            status=safe_status
        )
    except KeyError as exc:
        # The template is missing a placeholder; re-raise with context.
        raise ValueError(f"PROFILE_FORMAT missing placeholder: {exc}") from exc

    return formatted_profile