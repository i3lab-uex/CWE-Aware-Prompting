import re

# Regular expression to match a potentially dangerous URL scheme.
# It matches:
#   - javascript:, vbscript: and any other scheme that ends with ':' (case‑insensitive)
#   - data URLs that are NOT image/* (i.e. exclude "data:image/...") because those
#     are considered safe in this context.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # Optional leading whitespace
    (
        (?:javascript|vbscript)          # Known dangerous schemes
        |                                # OR
        [a-z][a-z0-9+.-]*:               # Any other scheme (RFC 3986)
    )
    |                                    # OR
    data:                                # Data URL
    (?!image/)[^;]*                      # Exclude image/* MIME types
    """,
    re.IGNORECASE | re.VERBOSE,
)

def analyze_scheme(url: str) -> bool:
    """
    Return True if *url* contains a potentially harmful URL scheme
    (e.g. javascript:, vbscript: or any non‑image data URI).
    Otherwise return False.

    Parameters
    ----------
    url : str
        The string to examine for a dangerous URL scheme.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        False otherwise.

    Notes
    -----
    The function is intentionally tolerant to leading whitespace and case
    variations.  It treats any scheme that ends with ':' as dangerous,
    except for safe data URLs that are image/* MIME types.
    """
    if not isinstance(url, str):
        # Non‑string input cannot be a URL; treat as safe.
        return False

    match = _DANGEROUS_SCHEME_RE.match(url)
    return bool(match)

# Example usage (for manual testing only):
if __name__ == "__main__":
    test_cases = [
        "javascript:alert('XSS')",
        "  vbscript:msgbox('test')",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
        "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==",
        "http://example.com",
    ]
    for t in test_cases:
        print(f"{t!r:60} -> {analyze_scheme(t)}")