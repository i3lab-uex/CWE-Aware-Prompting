import re

# Regular expression for a reasonably strict URL validation.
_URL_REGEX = re.compile(
    r"""
    ^(?:(?:https?|ftp)://)                      # scheme
    (?:\S+(?::\S*)?@)?                         # optional user:pass@
    (?:                                         
        (?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+    # subdomains
        [A-Za-z]{2,63}                          # top‑level domain
    |   \d{1,3}(?:\.\d{1,3}){3}                 # or IPv4
    |   \[?[A-Fa-f0-9:]+\]?                     # or IPv6
    )
    (?::\d{1,5})?                               # optional port
    (?:/[^\s]*)?$                                # path and query, no whitespace
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Validate a URL string using a compiled regular expression.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False
    return bool(_URL_REGEX.fullmatch(link))