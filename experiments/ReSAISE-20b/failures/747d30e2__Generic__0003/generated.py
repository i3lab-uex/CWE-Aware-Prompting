import re

# Regular expression patterns for malicious URL schemes.
# We explicitly exclude data URLs that start with "data:image/".
MALICIOUS_SCHEMES = [
    r'^\s*javascript\s*:',
    r'^\s*jscript\s*:',
    r'^\s*vbscript\s*:'
]

# Combine patterns into a single regex for efficiency.
MALICIOUS_RE = re.compile(
    r'|'.join(MALICIOUS_SCHEMES),
    flags=re.IGNORECASE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Detect whether the supplied string contains a potentially malicious URL
    scheme such as javascript:, jscript:, or vbscript:.  Image data URLs
    starting with "data:image/" are explicitly ignored.

    Parameters
    ----------
    s : str
        The string to test for malicious URL schemes.

    Returns
    -------
    bool
        ``True`` if a malicious scheme is detected; otherwise ``False``.

    Notes
    -----
    * Leading whitespace before the scheme is allowed.
    * The function is case‑insensitive and trims surrounding whitespace
      before matching.
    """
    if not isinstance(s, str):
        return False

    # Exclude data URLs that point to images
    if s.strip().lower().startswith('data:image/'):
        return False

    # Search for any malicious scheme at the beginning of the string.
    return bool(MALICIOUS_RE.match(s))