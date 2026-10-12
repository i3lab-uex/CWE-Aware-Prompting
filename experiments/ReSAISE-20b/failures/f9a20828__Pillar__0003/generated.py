import re

# Compile the regex once for efficiency and to avoid repeated compilation.
# The pattern matches any URL scheme that starts with a known
# potentially dangerous keyword followed by a colon.
_DANGEROUS_SCHEMES = re.compile(
    r'^\s*('
    r'javascript|vbscript|data|file|mailto|ftp|telnet|ldap'
    r')\s*:',
    re.IGNORECASE
)

# The pattern that specifically matches a valid image data URL.
_IMAGE_DATA_URL = re.compile(
    r'^\s*data\s*:\s*image\/(?:png|jpeg|jpg|gif|bmp)\b',
    re.IGNORECASE
)


def analyze_scheme(url: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme.

    The function considers the following schemes as dangerous:
        javascript, vbscript, data (non-image), file, mailto,
        ftp, telnet, ldap

    Image data URLs (e.g. ``data:image/png;base64,...``) are treated as safe
    and will not cause the function to return ``True``.

    Parameters
    ----------
    url : str
        The string to examine.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme (excluding valid image data URLs),
        otherwise ``False``.

    Notes
    -----
    The function is deliberately tolerant to leading whitespace and
    case differences. It does not attempt to fully parse the URL, only
    performs a simple prefix check.
    """
    if not isinstance(url, str):
        # Non-string input is considered unsafe by default.
        return True

    # Quick check for valid image data URLs – these are explicitly allowed.
    if _IMAGE_DATA_URL.match(url):
        return False

    # Check for any dangerous scheme.
    if _DANGEROUS_SCHEMES.match(url):
        return True

    # No dangerous scheme found.
    return False