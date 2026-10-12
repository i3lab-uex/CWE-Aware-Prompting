import re

# Pre‑compiled regular expression for a valid HTTP/HTTPS URL.
# The pattern ensures the string starts with http:// or https://
# and contains at least one non‑whitespace character after that.
_URL_RE = re.compile(r'^(https?://)\S+$', re.IGNORECASE)


def verify_path_format(address: str) -> bool:
    """
    Verify whether the given string is a syntactically valid HTTP/HTTPS path.

    Parameters
    ----------
    address : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        ``True`` if the string matches the HTTP/HTTPS pattern, otherwise ``False``.

    Notes
    -----
    The function uses a pre‑compiled regular expression and performs a single
    full match.  This approach is O(n) in the length of *address* and does
    not suffer from catastrophic backtracking, mitigating CWE‑407 risks.
    """
    if not isinstance(address, str):
        # If the input is not a string we consider it invalid.
        return False

    # Perform a full match against the compiled pattern.
    return bool(_URL_RE.fullmatch(address))