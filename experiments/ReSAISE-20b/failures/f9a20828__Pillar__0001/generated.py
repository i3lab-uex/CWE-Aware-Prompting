import re

# Regular expression to capture the scheme of a URL (everything before the first colon).
_SCHEME_RE = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9+\-.]*):')

# List of schemes that are considered dangerous.
_DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'data',          # data URLs are handled separately
    'file',
    'mailto',
    'ftp',
    'tel',
}

# Regular expression to detect a valid image data URL (data:image/...).
_IMAGE_DATA_RE = re.compile(
    r'^\s*data\s*:\s*image\/[a-zA-Z0-9\-\+]+', re.IGNORECASE
)

def analyze_scheme(url: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme.
    
    The function returns True if the string starts with a dangerous scheme
    (e.g. javascript:, vbscript:) other than valid image data URLs.
    
    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.
    
    Returns
    -------
    bool
        True if a potentially harmful scheme is detected, False otherwise.
    
    Notes
    -----
    - Leading/trailing whitespace is ignored.
    - Data URLs that represent images are considered safe and do not trigger
      a True result.
    
    Raises
    ------
    re.error
        If the underlying regular expression fails to compile.
    """
    if not isinstance(url, str):
        return False  # Non-string input is treated as safe.

    # Check for a valid image data URL first.
    if _IMAGE_DATA_RE.match(url):
        return False

    # Extract the scheme, if any.
    match = _SCHEME_RE.match(url)
    if not match:
        return False  # No scheme present.

    scheme = match.group(1).lower()
    
    # If the scheme is in our list of dangerous schemes, flag it.
    if scheme in _DANGEROUS_SCHEMES:
        # Exclude data URLs that are not images.
        if scheme == 'data':
            return False
        return True

    # All other schemes are considered safe for this check.
    return False