import re

# Regular expression that matches a dangerous URL scheme.
#
#   1. The string must start with an optional whitespace or the beginning of
#      the string.
#   2. The scheme must be one of: javascript, vbscript, data (with a
#      non‑image MIME type) or any other scheme that is not explicitly allowed.
#   3. For data URLs we allow only image/* MIME types; any other data URL is
#      considered dangerous.
#
# The pattern is intentionally conservative: it matches the whole string so
# that any part of a URL containing a dangerous scheme will cause the
# function to return True.
_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                                 # optional leading whitespace
    (
        (?:javascript|vbscript)          # explicit dangerous schemes
      | data:(?!image/)[^;]*            # any data: scheme that is NOT an image
      | (?!https?://|mailto:)[a-z][^:\s]*   # any other scheme that is not http/https/mailto
    )
    ''',
    re.IGNORECASE | re.VERBOSE
)

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether the given string contains a potentially harmful URL
    scheme (e.g., javascript:, vbscript:, or any non‑image data: URL).

    Parameters
    ----------
    url_str : str
        The string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # A quick early exit for None or empty strings
    if not url_str:
        return False

    # If the regex finds a match, we consider the string dangerous.
    return bool(_DANGEROUS_SCHEME_RE.search(url_str))