import re

# Regular expression that matches a typical HTTP/HTTPS URL.
# It requires the scheme, at least one character for the host,
# and allows optional paths, query strings, and fragments.
_URL_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme followed by ://
    [^\s/]+                     # at least one non-space character for the host
    (?:/[^\s]*)?                # optional path and anything after it
    $                           # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def verify_link(link: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if the string matches a basic HTTP/HTTPS URL pattern,
        otherwise False.

    Notes
    -----
    - The function performs a simple structural check; it does not attempt
      DNS resolution or other network operations.
    - No exceptions are raised for malformed input; an empty string
      or non-string input will simply return False.
    """
    if not isinstance(link, str):
        return False
    return bool(_URL_RE.match(link))