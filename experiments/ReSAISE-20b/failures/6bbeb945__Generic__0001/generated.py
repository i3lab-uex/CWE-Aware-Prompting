import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Determine whether a URI string contains a potentially dangerous scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    # Normalize leading whitespace and make the regex case‑insensitive
    uri = uri_str.lstrip()

    # 1. Directly disallowed schemes
    if re.match(r'^(javascript|vbscript):', uri, flags=re.IGNORECASE):
        return True

    # 2. Data URIs that are NOT image/* (i.e., potentially executable)
    if re.match(r'^data:', uri, flags=re.IGNORECASE):
        # Extract the media type part of the data URI
        match = re.match(r'^data:([^;,\s]+)', uri, flags=re.IGNORECASE)
        if match:
            media_type = match.group(1).lower()
            # If the media type is not an image, consider it dangerous
            if not media_type.startswith('image/'):
                return True

    # No dangerous scheme detected
    return False