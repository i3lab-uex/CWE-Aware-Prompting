import re

# Regular expression to validate a typical HTTP/HTTPS URL.
# It covers:
#   - scheme: http or https
#   - host: domain with optional subdomains, IP address, or localhost
#   - port (optional)
#   - path/query/fragment (optional)
_URL_REGEX = re.compile(
    r"""
    ^(?:https?)://                                  # http:// or https://
    (?:                                              
        (?:(?P<user>[^:@/]+)(?::(?P<pwd>[^@/]*))?@)?  # optional user:pass@
        (?P<host>
            (?:[a-zA-Z0-9\-\.]+)                     # domain
            |                                        # or
            \d{1,3}(?:\.\d{1,3}){3}                  # IPv4
            |                                        # or
            localhost                               # localhost
        )
        (?::(?P<port>\d{1,5}))?                      # optional port
    )
    (?P<path>/[^\s?#]*)?                              # path
    (?:\?(?P<query>[^\s#]*))?                        # query string
    (?:\#(?P<fragment>.*))?                          # fragment
    $                                                 # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Validate that the given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    # Guard against non‑string input
    if not isinstance(path_string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    match = _URL_REGEX.fullmatch(path_string.strip())
    return bool(match)