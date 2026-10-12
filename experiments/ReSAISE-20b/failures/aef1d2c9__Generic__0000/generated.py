import re

def has_script_scheme(url: str) -> bool:
    """
    Detect whether a string contains a dangerous URL scheme such as
    'javascript:' or 'vbscript:'.  Valid image data URLs (e.g. data:image/png;base64,...) are ignored.

    Parameters
    ----------
    url : str
        The string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    if not isinstance(url, str):
        return False

    # Strip leading/trailing whitespace and normalize case for comparison
    url = url.strip()
    if not url:
        return False

    # Extract the scheme part (everything before the first colon)
    scheme_match = re.match(r'^\s*([a-zA-Z][a-zA-Z0-9+.-]*)\s*:?', url)
    if not scheme_match:
        return False

    scheme = scheme_match.group(1).lower()

    # Dangerous schemes list
    dangerous_schemes = {'javascript', 'vbscript'}

    if scheme in dangerous_schemes:
        return True

    # Handle data URLs – only consider them safe if they are image/* types
    if scheme == 'data':
        # data URL syntax: data:[<mediatype>][;base64],<data>
        # Extract the media type if present
        data_match = re.match(r'^data\s*:\s*([^,;]+)', url, re.IGNORECASE)
        if data_match:
            media_type = data_match.group(1).strip().lower()
            # If the media type is not an image, treat it as dangerous
            if not media_type.startswith('image/'):
                return True
        else:
            # Malformed data URL – treat as dangerous
            return True

    return False