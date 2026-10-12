import re

# Regular expression for a basic HTTP/HTTPS URL.
# It requires the scheme, "http://" or "https://", followed by a non‑empty host
# and optional path/query/fragment, but forbids whitespace.
_HTTP_URL_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme + ://
    [^\s/]+                     # host (at least one non‑space, non‑slash character)
    (?:/[^\s]*)?                # optional path and everything after it, no whitespace
    $                           # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def path_check(u: str) -> bool:
    """
    Validate that a string is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if the input is a valid http/https URL, False otherwise.

    Notes
    -----
    The function never raises an exception; any error (e.g., a non‑string
    argument) results in ``False``.  The regex is intentionally simple to avoid
    the pitfalls of full URL parsing (e.g., port numbers, IPv6 literals,
    percent‑encoding).  For more comprehensive validation consider using
    ``urllib.parse`` or a dedicated URL parsing library.
    """
    if not isinstance(u, str):
        return False
    return bool(_HTTP_URL_RE.fullmatch(u))