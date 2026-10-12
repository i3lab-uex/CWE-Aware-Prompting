import re

# Regular expression that matches dangerous URL schemes.
# It allows optional surrounding whitespace, optional quotes or angle brackets,
# and is case‑insensitive.  The pattern captures the scheme name.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                # optional leading whitespace
    (?:[\'"\(<]?\s*)?   # optional opening quote, bracket or angle bracket
    (?P<scheme>         # capture the scheme name
        javascript
      | vbscript
      | data          # handle data: URLs specially
    )
    \s*:\s*             # colon separator with optional whitespace
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression that matches a valid image data URL.
_IMAGE_DATA_RE = re.compile(
    r"^data\s*:\s*image/[^;]+;base64,",
    re.IGNORECASE,
)


def has_script_scheme(url: str) -> bool:
    """
    Return True if *url* contains a potentially dangerous URL scheme
    (e.g. ``javascript:`` or ``vbscript:``) while ignoring valid image
    data URLs such as ``data:image/png;base64,...``.

    Parameters
    ----------
    url : str
        The string to test.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # Quick guard for non‑string input
    if not isinstance(url, str):
        return False

    # First check for a data: URL; if it is an image data URL we return False
    if _IMAGE_DATA_RE.match(url.strip()):
        return False

    # Search for dangerous schemes
    match = _DANGEROUS_SCHEME_RE.search(url)
    if not match:
        return False

    scheme = match.group("scheme").lower()
    # Reject only if it is a known dangerous scheme
    return scheme in {"javascript", "vbscript"}