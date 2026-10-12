import re

# Regular expression that matches any URL scheme (e.g. javascript:, vbscript:)
# but ignores the safe data:image/… URLs.
_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                      # optional leading whitespace
    (?!data:image/[^;]*;)     # negative look‑ahead: not a data:image URL
    ([a-z][a-z0-9+\-.]*):     # scheme name followed by a colon
    ''',
    re.IGNORECASE | re.VERBOSE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the supplied string contains a potentially harmful
    URL scheme, excluding safe image-based data URLs.

    Parameters:
        input_url (str): The string to examine.

    Returns:
        bool: True if a dangerous scheme is detected, False otherwise.
    """
    # If the regex finds a match that is not a safe data:image URL, it
    # indicates a potentially malicious scheme.
    return bool(_DANGEROUS_SCHEME_RE.match(input_url))