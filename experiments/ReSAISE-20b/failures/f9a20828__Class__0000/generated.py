import re

# Regular expression to detect potentially dangerous URL schemes.
# The pattern matches a string that starts with an optional
# whitespace, followed by a scheme name (javascript, vbscript,
# or data), a colon and optional whitespace.  The `data` scheme
# is handled specially later to allow only image data URLs.
_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(?P<scheme>javascript|vbscript|data)\s*:', re.IGNORECASE
)

def analyze_scheme(url: str) -> bool:
    """
    Determine whether the supplied URL contains a potentially
    dangerous scheme, excluding safe image data URLs.

    Parameters
    ----------
    url : str
        The URL string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    # Quick check for empty or non-string input
    if not isinstance(url, str) or not url:
        return False

    match = _DANGEROUS_SCHEME_RE.match(url)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # If the scheme is 'data', ensure it is an image data URL.
    if scheme == 'data':
        # The rest of the string after 'data:' starts with
        # optional media type and parameters.  We allow only
        # image/* MIME types.
        rest = url[match.end():].lstrip()
        if rest.lower().startswith('image/'):
            return False
        # Any other data: scheme is considered dangerous.
        return True

    # For javascript or vbscript schemes, any appearance is dangerous.
    return True