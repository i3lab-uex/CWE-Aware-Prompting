import re

# Regular expression that matches common malicious URL schemes.
# It ignores valid data URLs (e.g., "data:image/png;base64,...").
_MALICIOUS_SCHEME_RE = re.compile(
    r"""(?i)              # case-insensitive
        ^\s*               # optional leading whitespace
        (?:javascript|vbscript)   # dangerous schemes to detect
        \s*:\s*            # colon separator with optional whitespace
    """,
    re.VERBOSE,
)

# Regular expression that matches valid data URLs for images.
_DATA_URL_RE = re.compile(
    r"""(?i)              # case-insensitive
        ^\s*data:image/  # data URL for images
    """,
    re.VERBOSE,
)

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detect whether the supplied string contains a malicious URL scheme.

    Parameters
    ----------
    url_string : str
        The input string to be inspected for potentially malicious URL schemes.

    Returns
    -------
    bool
        True if the string contains any dangerous URL scheme (e.g., 'javascript:' or
        'vbscript:') and is not a valid image data URL; otherwise False.

    Notes
    -----
    The function performs the check in a single pass and is resilient to leading
    whitespace.  It does not raise any exceptions for normal inputs, but a malformed
    regular expression would surface as `re.error`.
    """
    # Quick exit for empty input.
    if not url_string:
        return False

    # If it's a valid image data URL, we consider it safe.
    if _DATA_URL_RE.match(url_string):
        return False

    # Check for dangerous schemes.
    return bool(_MALICIOUS_SCHEME_RE.search(url_string))