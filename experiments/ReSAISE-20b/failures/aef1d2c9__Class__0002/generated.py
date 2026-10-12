import re

def has_script_scheme(url: str) -> bool:
    """
    Detect whether the supplied URL contains a potentially dangerous
    scheme (e.g., javascript:, vbscript:) while ignoring valid image data URLs.

    Parameters
    ----------
    url : str
        The URL string to inspect.

    Returns
    -------
    bool
        True if a risky scheme is detected; False otherwise.
    """
    # Strip leading whitespace to avoid matching in the middle of a string
    trimmed = url.lstrip()

    # Regex to capture the scheme part before the colon
    match = re.match(r'^([a-z][a-z0-9+\-.]*):', trimmed, flags=re.IGNORECASE)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Dangerous schemes
    dangerous = {'javascript', 'vbscript'}

    if scheme in dangerous:
        return True

    # Handle data URLs: only treat as dangerous if not an image
    if scheme == 'data':
        # A valid image data URL starts with "data:image/"
        if trimmed.lower().startswith('data:image/'):
            return False
        # Any other data URL is considered risky
        return True

    return False