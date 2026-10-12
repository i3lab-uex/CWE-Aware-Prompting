import re

# Pre‑compiled regex that matches a well‑formed http or https URL.
# The pattern is deliberately simple to avoid catastrophic backtracking
# (CWE‑407) and to keep the worst‑case complexity linear in the length of
# the input string.
_URL_RE = re.compile(
    r'''
    ^                                   # start of string
    (?:http|https)://                   # protocol
    [^\s/]+                             # host (no whitespace or slash)
    (?:/[^\s]*)?                        # optional path and query
    $                                   # end of string
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid http or https URL.

    Parameters
    ----------
    link : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the expected URL format, False otherwise.
    """
    try:
        return _URL_RE.fullmatch(link) is not None
    except Exception:
        # In the unlikely event that an unexpected error occurs,
        # return False instead of propagating the exception.
        return False