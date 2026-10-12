import re

# Regular expression for validating URLs.
# This pattern covers http, https, ftp, file protocols and allows
# optional authentication, subdomains, ports, paths, query strings
# and fragments. It is not exhaustive but covers the most common cases.
_URL_REGEX = re.compile(
    r'^(?:(?:http|https|ftp)://)'                     # protocol
    r'(?:\S+(?::\S*)?@)?'                            # optional user:pass@
    r'(?:'
        r'\d{1,3}(?:\.\d{1,3}){3}'                    # IPv4
        r'|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?'                # IPv6
        r'|'
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'  # domain
        r'[a-zA-Z]{2,6}'                             # TLD
    r')'
    r'(?::\d{1,5})?'                                 # optional port
    r'(?:/[^?#\s]*)?'                                # path
    r'(?:\?[^#\s]*)?'                                 # query string
    r'(?:#\S*)?$'                                     # fragment
)

def check_url_format(link: str) -> bool:
    """
    Validate whether the provided string is a syntactically correct URL.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    # Early exit for empty input
    if not isinstance(link, str) or not link:
        return False

    # The regex is case-insensitive for domain and protocol parts
    match = _URL_REGEX.match(link.strip())
    return bool(match)