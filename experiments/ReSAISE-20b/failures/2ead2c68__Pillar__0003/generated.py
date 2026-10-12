import re

# Regular expression that matches a typical http or https URL.
# It allows any non‑whitespace characters after the protocol,
# ensuring the string is a single, well‑formed URL.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https protocol
    [^\s/$.?#].[^\s]*                   # at least one non‑whitespace character after the protocol
    $                                   # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def path_verification(link: str) -> bool:
    """
    Return True if `link` is a valid http or https URL, False otherwise.
    
    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the input matches the HTTP/HTTPS pattern, False otherwise.
    
    Notes
    -----
    The function never raises an exception; any errors are silently handled by returning False.
    """
    try:
        return bool(_URL_RE.fullmatch(link))
    except Exception:
        # In the unlikely event that an exception occurs (e.g., invalid input type),
        # we return False to avoid propagating the error.
        return False