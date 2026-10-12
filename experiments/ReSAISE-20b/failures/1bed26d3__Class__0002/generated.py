import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine if a string contains a potentially dangerous URL scheme.

    The function checks for the following schemes:
        - javascript
        - vbscript
        - data (excluding image-based data URLs)

    Parameters
    ----------
    url_str : str
        The URL string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is found (excluding safe image data URLs),
        False otherwise.

    Raises
    ------
    re.error
        If the regular expression fails to compile or match.
    """
    # Normalise whitespace at the start
    trimmed = url_str.lstrip()

    # Regex to capture the scheme before any colon
    scheme_match = re.match(r'(?i)^([a-z]+)\s*:', trimmed)
    if not scheme_match:
        return False

    scheme = scheme_match.group(1).lower()

    # Dangerous schemes
    if scheme in ('javascript', 'vbscript'):
        return True

    # Handle data URLs
    if scheme == 'data':
        # Extract the media type part of the data URL
        # Example: "data:image/png;base64,..." or "data:text/html;charset=utf-8,..."
        # We want to exclude image types.
        media_type = trimmed[5:].split(';', 1)[0]  # after 'data:' up to first ';'
        if media_type.lower().startswith('image/'):
            return False  # safe image data URL
        else:
            return True   # other data URLs are considered dangerous

    # All other schemes are considered safe
    return False