import re

# Regular expression to match dangerous schemes at the start of a string.
# It ignores leading whitespace and checks for common malicious protocols
# such as javascript: or vbscript:.  The regex is case‑insensitive.
_DANGEROUS_SCHEMES_RE = re.compile(r'^\s*(javascript|vbscript)\b', re.IGNORECASE)

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detect whether *url_string* contains a potentially dangerous URL scheme.
    
    The function checks for the presence of malicious schemes such as
    `javascript:` or `vbscript:` at the beginning of the string.  It also
    considers `data:` URLs to be potentially dangerous unless they are
    specifically image data URLs (`data:image/...`).  Leading whitespace
    is ignored.

    Parameters
    ----------
    url_string : str
        The string to be inspected for malicious URL schemes.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found, otherwise ``False``.

    Notes
    -----
    The function does not raise exceptions for normal usage.  A ``re.error``
    may be raised if the compiled regex pattern is invalid, but this
    should not happen with the current hard‑coded pattern.
    """
    if not isinstance(url_string, str):
        # Non-string inputs are considered safe (no scheme to inspect).
        return False

    # 1. Check for javascript: or vbscript: schemes.
    if _DANGEROUS_SCHEMES_RE.match(url_string):
        return True

    # 2. Check for data: URLs that are not image data.
    lower = url_string.lower().lstrip()
    if lower.startswith('data:'):
        # Allow data URLs that are explicitly image data.
        if not lower.startswith('data:image/'):
            return True

    # No dangerous scheme detected.
    return False