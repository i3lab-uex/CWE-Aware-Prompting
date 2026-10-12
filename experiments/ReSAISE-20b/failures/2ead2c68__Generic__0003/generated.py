import re

# Regular expression that matches a basic HTTP/HTTPS URL.
# It checks for the scheme, at least one character in the host,
# and allows optional path/query/fragment components.
_HTTP_URL_RE = re.compile(
    r'^https?://'          # http:// or https://
    r'(?:[A-Za-z0-9.-]+)'  # host: letters, digits, dots and hyphens
    r'(?:\:[0-9]+)?'       # optional port
    r'(?:/[^ \t\r\n]*)?$'  # optional path/query/fragment
)

def path_verification(link: str) -> bool:
    """
    Verify that the input string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if `link` matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False
    return bool(_HTTP_URL_RE.match(link))