import re

# Regular expression to match dangerous URL schemes.
# It matches any string that starts with a scheme (letters, digits, +,-,.)
# followed by ':' and is NOT a safe data:image URL.
DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                               # optional leading whitespace
    (                                   # start capturing group for scheme
        (?P<scheme>[a-z0-9+.-]+)       # scheme name (RFC 3986)
    )
    \s*:\s*                            # colon separating scheme from rest
    (?!data\s*:\s*image/[^;]*;?)       # negative look‑ahead: safe data:image URLs
    ''',
    re.IGNORECASE | re.VERBOSE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Return True if the input string contains a potentially malicious URL scheme
    (e.g., javascript:, vbscript:) and is not an image-based data URI.
    
    Parameters
    ----------
    input_url : str
        The string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is detected; False otherwise.
    """
    # Fast path: empty or non-string inputs
    if not isinstance(input_url, str) or not input_url:
        return False

    # Search for a dangerous scheme at the beginning of the string.
    match = DANGEROUS_SCHEME_RE.match(input_url)
    if not match:
        return False

    # Extract the scheme name and normalise it to lower case.
    scheme = match.group('scheme').lower()

    # List of known safe schemes that are not considered malicious.
    SAFE_SCHEMES = {'data', 'mailto', 'tel', 'file', 'http', 'https', 'ftp'}

    # If the scheme is not in the safe list, it's malicious.
    return scheme not in SAFE_SCHEMES