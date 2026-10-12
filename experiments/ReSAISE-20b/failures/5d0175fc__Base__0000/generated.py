import re

# Compile a simple, non‑catastrophic regular expression for HTTP/HTTPS URLs
_URL_REGEX = re.compile(
    r"""
    ^https?://                 # http or https scheme
    [A-Za-z0-9.-]+             # domain name (letters, digits, dots and hyphens)
    (?::\d+)?                  # optional port
    (?:/[^\s]*)?               # optional path/query/fragment, no whitespace allowed
    $
    """,
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify that *address* is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate as a URL.

    Returns
    -------
    bool
        ``True`` if the string matches the HTTP/HTTPS URL pattern,
        otherwise ``False``.

    Notes
    -----
    The function performs a simple syntactic check and does **not** perform
    network operations or DNS lookups.  It is intentionally conservative to
    avoid excessive back‑tracking and potential denial‑of‑service attacks.
    """
    if not isinstance(address, str):
        return False
    # Use fullmatch to ensure the entire string matches the pattern.
    return _URL_REGEX.fullmatch(address) is not None