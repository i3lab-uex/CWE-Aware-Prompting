import re

# Regex to capture the scheme part of a URL (everything before ':')
_SCHEME_RE = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9+\-.]*):')

# Set of known harmless schemes (currently only image data URLs)
_HARNESS_SCHEMES = {'data'}

# Set of potentially dangerous schemes that should trigger detection
_DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'data',          # treated specially below
    'file',
    'ftp',
    'mailto',
    'mhtml',
    # Add more as needed
}

def detect_js_scheme(url_string: str) -> bool:
    """
    Detects whether a given string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme, aside from
        valid image data URLs; False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading whitespace and extract the scheme
    match = _SCHEME_RE.match(url_string)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Ignore image data URLs: data:image/...
    if scheme == 'data':
        # Check for the specific image MIME type
        data_uri_match = re.match(r'^\s*data\s*:\s*image/[^;]+', url_string, re.IGNORECASE)
        if data_uri_match:
            return False
        # Any other data: scheme is considered dangerous
        return True

    # If the scheme is in our dangerous set, flag it
    if scheme in _DANGEROUS_SCHEMES:
        return True

    # All other schemes are considered safe
    return False