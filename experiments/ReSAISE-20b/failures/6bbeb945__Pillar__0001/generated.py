import re

# Regular expression to capture the scheme part of a URI.
_SCHEME_RE = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9+.-]*):', re.I)

# Regular expression to detect image data URLs (safe).
_IMAGE_DATA_RE = re.compile(r'^\s*data\s*:\s*image/', re.I)

# Set of schemes considered dangerous. 'data' is handled separately.
_DANGEROUS_SCHEMES = {'javascript', 'vbscript'}

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        True if the URI contains a dangerous scheme; False otherwise.

    Raises
    ------
    re.error
        If an invalid regular expression is used (unlikely in this static code).
    """
    if not isinstance(uri_str, str):
        # Non-string inputs are considered safe for the purpose of this check.
        return False

    match = _SCHEME_RE.match(uri_str)
    if not match:
        # No scheme present; nothing dangerous here.
        return False

    scheme = match.group(1).lower()

    # Image data URLs are explicitly allowed.
    if scheme == 'data' and _IMAGE_DATA_RE.match(uri_str):
        return False

    # Any other scheme in the dangerous list is considered a threat.
    return scheme in _DANGEROUS_SCHEMES