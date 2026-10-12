import re

# Regex to detect potentially dangerous URL schemes.
# It matches any scheme that starts with a word (letters, digits, +, -, .)
# followed by ':' and ignores image data URLs.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # optional leading whitespace
    (?:                                   # start non-capturing group for the scheme
        (?P<scheme>[a-z0-9+\-.]+)         # capture the scheme
    )
    :                                     # literal colon after the scheme
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regex to ignore image data URLs (data:image/...).
_DATA_URL_RE = re.compile(
    r"""
    ^\s*                                 # optional leading whitespace
    data:\s*image/                       # data:image/
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Set of known dangerous schemes.
_DANGEROUS_SCHEMES = {
    "javascript",
    "vbscript",
    "data",      # data: is dangerous unless it is an image
    "file",
    "ftp",
    "mailto",
}

def analyze_scheme(url: str) -> bool:
    """
    Return True if the given string contains a potentially harmful URL scheme
    (e.g. javascript:, vbscript:) while ignoring safe image data URLs.
    
    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.
    
    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        False otherwise.
    
    Notes
    -----
    - The function is case‑insensitive and ignores leading whitespace.
    - Image data URLs (e.g. data:image/png;base64,...) are considered safe
      and will return False.
    - If the string is not a URL or does not contain a scheme, it returns
      False.
    """
    if not isinstance(url, str):
        return False

    # Skip safe image data URLs.
    if _DATA_URL_RE.match(url):
        return False

    m = _DANGEROUS_SCHEME_RE.match(url)
    if not m:
        return False

    scheme = m.group("scheme").lower()
    # If the scheme is in the dangerous list and not an image data URL,
    # consider it harmful.
    return scheme in _DANGEROUS_SCHEMES