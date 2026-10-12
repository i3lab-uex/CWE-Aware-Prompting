import re

# Regular expression to detect dangerous URL schemes.
#  - javascript: and vbscript: (case‑insensitive) are considered dangerous.
#  - data: URLs are allowed only if they specify an image type (e.g., data:image/png,...).
#    Any other data: scheme is considered dangerous.
DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                   # optional leading whitespace
    (?:                                    # non‑capturing group for the two checks
        (?i:javascript|vbscript)           # javascript or vbscript (case‑insensitive)
        |                                  # OR
        data:(?!image\b)                   # data: but not followed by 'image'
    )
    \b
    """,
    re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if *user_input* contains a potentially dangerous URL scheme,
    excluding valid image data URLs. The function is resilient against
    malformed inputs and does not raise exceptions for typical usage.

    Parameters
    ----------
    user_input : str
        The string to inspect for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    if not isinstance(user_input, str):
        # Non‑string inputs are considered safe; they cannot contain a URL scheme.
        return False

    # The regex is anchored to the start of the string and ignores leading
    # whitespace.  It will match "javascript:", "vbscript:" or any data: URL
    # that is not an image.  All other schemes are ignored.
    return bool(DANGEROUS_SCHEME_RE.search(user_input))