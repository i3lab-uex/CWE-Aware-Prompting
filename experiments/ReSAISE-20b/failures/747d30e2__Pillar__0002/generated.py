import re

# Regular expression to detect potentially malicious URL schemes.
# It matches common schemes such as javascript:, jscript:, vbscript: etc.,
# but explicitly excludes data URLs that point to image MIME types.
_MALICIOUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                  # optional leading whitespace
    (?:                                   # start non-capturing group for schemes
        javascript:                       # "javascript:" scheme
      | jscript:                          # "jscript:" scheme
      | vbscript:                         # "vbscript:" scheme
      | lscript:                          # "lscript:" scheme (rare)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

# Regular expression to detect data URLs that refer to images.
_DATA_IMAGE_RE = re.compile(
    r"""
    ^\s*data:                              # data URL scheme
    \s*                                    # optional whitespace
    image/                                 # MIME type starts with "image/"
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if the string `s` contains a potentially malicious URL scheme
    (e.g., javascript:, jscript:, vbscript:) while explicitly excluding image
    data URLs. Otherwise, return False.

    Parameters:
        s (str): The string to be examined.

    Returns:
        bool: True if a malicious scheme is detected, False otherwise.
    """
    # Fast path for empty or non-string inputs
    if not isinstance(s, str) or not s:
        return False

    # Reject image data URLs first
    if _DATA_IMAGE_RE.match(s):
        return False

    # Check for malicious schemes
    return bool(_MALICIOUS_SCHEME_RE.match(s))