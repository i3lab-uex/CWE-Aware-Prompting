import re

# Pre‑compiled, non‑capturing pattern that matches a full HTTP/HTTPS URL
# without any capturing groups to avoid backtracking pitfalls.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme
    [a-zA-Z0-9.-]+                      # domain (letters, digits, dots, hyphens)
    (?::\d+)?                           # optional port
    (?:/[^\s]*)?                        # optional path/query/fragment, no whitespace
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)


def path_verification(link: str) -> bool:
    """
    Validate whether the provided string is a well‑formed HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        ``True`` if *link* matches the URL pattern, otherwise ``False``.

    Notes
    -----
    The function never raises exceptions. Invalid input (e.g., ``None`` or
    non‑string types) is treated as a non‑match and simply returns ``False``.
    """
    if not isinstance(link, str):
        return False
    return bool(_URL_RE.fullmatch(link))