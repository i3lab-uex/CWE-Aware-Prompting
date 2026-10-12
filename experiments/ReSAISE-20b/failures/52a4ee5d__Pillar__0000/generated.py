import re

# Regular expression that matches a URL scheme (e.g. javascript:, vbscript:, data:, etc.)
# We ignore image data URLs that start with "data:image/".
# The pattern is case‑insensitive and allows optional whitespace before the scheme.
# Example matches: "javascript:", "vbscript :", "data:text/plain,"
# Non‑matches: "data:image/png;base64,..."
_JS_SCHEME_RE = re.compile(
    r"""
    ^\s*                      # optional leading whitespace
    (?P<scheme>[a-zA-Z][a-z0-9+\-.]*)   # scheme part
    \s*:\s*                   # colon separator with optional whitespace
    (?!image\/)               # negative lookahead: not followed by "image/"
    """,
    re.IGNORECASE | re.VERBOSE
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect if a string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        except for valid image data URLs; False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    match = _JS_SCHEME_RE.match(url_string)
    if not match:
        return False

    scheme = match.group('scheme').lower()
    # Treat known safe schemes (e.g., http, https, mailto) as non‑dangerous.
    # Everything else is considered potentially harmful.
    safe_schemes = {'http', 'https', 'mailto', 'ftp', 'ftps', 'file'}
    return scheme not in safe_schemes