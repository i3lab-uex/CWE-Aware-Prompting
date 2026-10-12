import re

# Regular expression for validating URLs (RFC 3986 simplified)
_URL_RE = re.compile(
    r'^(?:http|https)://'          # scheme
    r'(?:\S+(?::\S*)?@)?'         # optional username:password@
    r'(?:[A-Za-z0-9.-]+|\[[^\]]+\])'  # host or IPv6
    r'(?:\:\d+)?'                 # optional port
    r'(?:/[^?#]*)?'               # path
    r'(?:\?[^#]*)?'               # query
    r'(?:#.*)?$'                  # fragment
)

def check_url_format(link: str) -> bool:
    """
    Verify whether a given string is a valid HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if `link` matches the URL pattern, False otherwise.
    """
    # Guard against non-string inputs
    if not isinstance(link, str):
        return False

    # Empty strings are considered invalid URLs
    if not link:
        return False

    # Perform the regex match; re.match is safe here because pattern anchors ^$
    return bool(_URL_RE.match(link))