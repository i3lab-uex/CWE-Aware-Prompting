import re

# Regex that matches dangerous URL schemes but excludes valid image data URLs.
# It is case‑insensitive and allows optional whitespace before the scheme,
# ensuring we catch patterns like "  javascript:alert(1)".
_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                             # Optional leading whitespace
    (                               # Start capturing group for the scheme
        javascript:|                #   "javascript:" scheme
        vbscript:|                  #   "vbscript:" scheme
        data:(?!image/)[^;]+;       #   Any other "data:" scheme that is NOT an image
    )
    ''',
    re.IGNORECASE | re.VERBOSE,
)

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects whether a given string contains a potentially malicious URL scheme.

    The function looks for the following schemes:
        * javascript:
        * vbscript:
        * data: (excluding image data URLs)

    Parameters
    ----------
    url_string : str
        The string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    if not isinstance(url_string, str):
        # Non‑string inputs are considered safe by definition.
        return False

    # Search for the pattern anywhere in the string
    return bool(_DANGEROUS_SCHEME_RE.search(url_string))