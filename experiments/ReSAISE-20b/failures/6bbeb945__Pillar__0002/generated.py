import re

# Regular expression that matches common dangerous URI schemes.
# It is case‑insensitive and ignores leading whitespace.
_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(?P<scheme>javascript|vbscript|data)\b',
    re.IGNORECASE
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detects if a string contains a potentially dangerous URL scheme.

    The function looks for the following schemes:
        * javascript
        * vbscript
        * data

    Image based data URLs (e.g. ``data:image/png;base64,...``) are considered
    safe and do not trigger a True result.

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is present (excluding safe image data URLs),
        otherwise False.
    """
    # Quick exit for empty or non-string inputs
    if not isinstance(uri_str, str) or not uri_str:
        return False

    match = _DANGEROUS_SCHEME_RE.match(uri_str)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # If the scheme is 'data', ensure it is not an image data URL
    if scheme == 'data':
        # Allow only safe image data URLs (e.g., data:image/png;base64,...)
        if re.match(r'^\s*data\s*:\s*image\/', uri_str, re.IGNORECASE):
            return False
        # All other data: schemes are considered dangerous
        return True

    # For javascript and vbscript schemes, we consider them dangerous
    return True