import re

# Regular expression to validate http/https URLs.
# It covers:
#   - scheme: http or https
#   - hostname (IPv4/IPv6 literal, domain name)
#   - optional port
#   - optional path (no query or fragment for simplicity)
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme + '://'
    (?:                                 # start hostname group
        [A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?   # domain name
        |                               # or IPv6 literal in brackets
        \[[0-9a-fA-F:]+\]
    )
    (?: :\d{1,5} )?                     # optional port
    (?: /[^\s?#]*)?                      # optional path (no query or fragment)
    $                                   # end of string
    """,
    re.VERBOSE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    site_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the string matches the http/https path structure, False otherwise.

    Notes
    -----
    No exceptions are raised by this function. If `site_path` is not a string,
    the function will return False.
    """
    if not isinstance(site_path, str):
        return False
    # Using fullmatch ensures the entire string matches the pattern.
    return bool(_URL_RE.fullmatch(site_path))