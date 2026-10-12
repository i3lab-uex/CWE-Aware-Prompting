import re

# Regular expression to detect dangerous schemes.
#   - Matches 'javascript:' or 'vbscript:' (case‑insensitive).
#   - Matches 'data:' URLs that are NOT image/*.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                           # Optional leading whitespace
    (?:                            # Non‑capturing group for the schemes
        javascript:               #   - 'javascript:' scheme
      | vbscript:                 #   - 'vbscript:' scheme
      | data:(?!image/)           #   - 'data:' scheme not followed by 'image/'
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Return True if *uri_str* contains a potentially dangerous URL scheme
    (javascript:, vbscript:, or data: that is not an image data URI).  Otherwise
    return False.

    Parameters
    ----------
    uri_str : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is present, False otherwise.
    """
    if not isinstance(uri_str, str):
        # Non‑string inputs are considered safe
        return False

    return bool(_DANGEROUS_SCHEME_RE.search(uri_str))