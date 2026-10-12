import re

# Regular expression to detect dangerous URL schemes.
# It matches:
#   * any scheme that starts with a letter and is followed by `:`
#   * common dangerous schemes like javascript:, vbscript:, data:
# It ignores case and allows leading whitespace.
# Data URLs that are images (data:image/...) are explicitly excluded
# by a negative lookahead.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                     # optional leading whitespace
    (?!data\s*:\s*image\/)                   # exclude safe image data URLs
    [a-z][a-z0-9+\-.]*\s*:\s*                 # scheme (e.g. javascript:, vbscript:, data:)
    """,
    re.IGNORECASE | re.VERBOSE
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Return True if `uri_str` contains a potentially dangerous URL scheme,
    except for safe image-based data URLs. Otherwise return False.

    Parameters
    ----------
    uri_str : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    # Defensive check: ensure the input is a string
    if not isinstance(uri_str, str):
        raise TypeError("uri_str must be a string")

    # Search from the beginning of the string for a dangerous scheme
    return bool(_DANGEROUS_SCHEME_RE.match(uri_str))