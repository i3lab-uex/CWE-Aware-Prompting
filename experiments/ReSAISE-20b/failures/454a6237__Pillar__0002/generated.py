import re

# Regular expression pattern that matches valid http or https URLs.
# It checks for the scheme, a valid hostname (including IPv4), optional port,
# and an optional path/query fragment. It does not validate the entire URL
# semantics (e.g., DNS resolution) but ensures a syntactically correct format.
_URL_PATTERN = re.compile(
    r"""
    ^                                   # start of string
    (?:https?)://                       # http or https scheme followed by ://
    (?:
        [A-Za-z0-9]                     # first character of hostname
        (?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?  # rest of hostname label
        (?:\.[A-Za-z]{2,})+            # dot-separated labels ending with TLD
        |
        \d{1,3}(?:\.\d{1,3}){3}         # IPv4 address
    )
    (?::\d{1,5})?                       # optional port (0-65535)
    (?:/[^\s]*)?                        # optional path/query/fragment
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Validate whether a given string is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    The function is intentionally conservative: it only checks the syntax
    of the URL. It does not perform network operations or DNS lookups.
    """
    if not isinstance(path_string, str):
        return False
    # Use fullmatch to ensure the entire string matches the pattern.
    try:
        return bool(_URL_PATTERN.fullmatch(path_string.strip()))
    except Exception:
        # Any unexpected error is treated as invalid input.
        return False