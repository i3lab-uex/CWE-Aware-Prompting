import re

# Regular expression to detect potentially dangerous URL schemes.
# It matches:
#   * "javascript:" or "vbscript:" (case‑insensitive)
#   * "data:" URLs that are NOT image data URLs
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # optional leading whitespace
    (?:                                  # start non‑capturing group for schemes
        javascript:                     # javascript:
      | vbscript:                       # vbscript:
      | data:(?!image/)[^;,\s]+         # data: URLs that do NOT start with image/
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
        ``True`` if the string contains a dangerous scheme (e.g. javascript,
        vbscript, or a non‑image data URL); ``False`` otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace to avoid false negatives.
    stripped = url_string.strip()

    return bool(_DANGEROUS_SCHEME_RE.match(stripped))