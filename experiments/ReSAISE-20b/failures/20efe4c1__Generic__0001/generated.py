import re

# Regular expression to detect dangerous URL schemes.
# It matches any scheme that starts with "javascript" or "vbscript"
# (case‑insensitive) and ignores data URLs that start with "data:image".
DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                      # optional leading whitespace
    (?!data:image\b)          # negative lookahead to exclude image data URLs
    (?P<scheme>               # capture the scheme for clarity
        javascript\b
      | vbscript\b
    )
    \s*:                       # optional whitespace before the colon
    """,
    re.IGNORECASE | re.VERBOSE,
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether a string contains a potentially harmful URL scheme
    (e.g., "javascript:" or "vbscript:") while ignoring valid image data URLs.

    Parameters
    ----------
    url_input : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    # Quick guard for non-string input; return False rather than raising an exception.
    if not isinstance(url_input, str):
        return False

    # Strip leading/trailing whitespace to avoid false negatives.
    trimmed = url_input.strip()

    # Use the compiled regex to test for dangerous schemes.
    return bool(DANGEROUS_SCHEME_RE.search(trimmed))