import re

# Regular expression to detect potentially dangerous URL schemes.
# It matches URLs that start with javascript:, vbscript: or data:
# but it excludes valid image data URLs (data:image/...).
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # optional leading whitespace
    (?:
        javascript:                      # javascript scheme
      | vbscript:                        # vbscript scheme
      | data:
          (?!image/)[^;]*                # data: followed by anything except 'image/'
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect whether a string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_string : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme (javascript, vbscript,
        or data: URLs that are not image data URLs). False otherwise.

    Notes
    -----
    The function is intentionally tolerant of leading whitespace and case
    variations. It explicitly ignores image data URLs (e.g., "data:image/png;...").
    """
    if not isinstance(url_string, str):
        # If the input is not a string we cannot safely analyze it,
        # so return False to avoid false positives.
        return False

    # Strip leading/trailing whitespace for a cleaner match
    trimmed = url_string.strip()

    return bool(_DANGEROUS_SCHEME_RE.match(trimmed))