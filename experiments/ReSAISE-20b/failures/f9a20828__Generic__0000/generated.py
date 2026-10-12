import re

# Regular expression to detect potentially dangerous URL schemes.
# We ignore data URLs that are image types (e.g. data:image/png;base64,...).
_DANGEROUS_SCHEMES_RE = re.compile(
    r'''
    ^\s*                     # Optional leading whitespace
    (javascript|vbscript)     # Dangerous schemes
    \s*:\s*                  # Optional whitespace around the colon
    ''',
    re.IGNORECASE | re.VERBOSE,
)

_DATA_URL_RE = re.compile(
    r'''
    ^\s*                     # Optional leading whitespace
    data:                     # Data scheme
    \s*
    (?P<mediatype>[^;]+)     # Media type before the first semicolon
    ''',
    re.IGNORECASE | re.VERBOSE,
)

def analyze_scheme(url: str) -> bool:
    """
    Detect if a URL string contains a potentially harmful scheme such as
    javascript: or vbscript:.  Image data URLs (e.g. data:image/png;base64,...) are
    considered safe and do not trigger a positive result.

    Parameters
    ----------
    url : str
        The URL string to analyze.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme; False otherwise.
    """
    # Strip leading/trailing whitespace for safety
    url = str(url).strip()

    # Check for dangerous schemes first
    if _DANGEROUS_SCHEMES_RE.match(url):
        return True

    # Check for data URLs and allow only image types
    m = _DATA_URL_RE.match(url)
    if m:
        media_type = m.group('mediatype').lower()
        # Allow only image/* types
        if media_type.startswith('image/'):
            return False  # Safe data URL
        # Any other data type is considered safe for this check
        return False

    # No dangerous scheme detected
    return False