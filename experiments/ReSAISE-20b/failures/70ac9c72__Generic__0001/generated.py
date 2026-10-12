import re

# Regular expression for a minimal, but reasonably strict, HTTP/HTTPS URL.
# It matches:
#   - scheme: http or https
#   - "://"
#   - host: at least one non‑space character that is not a slash
#   - optional path, query or fragment starting with '/' , '?' or '#'
_URL_REGEX = re.compile(
    r"""
    ^(?P<scheme>https?)://               # http or https
    (?P<host>[^\s:/?#]+)                 # host (no spaces, slashes or query chars)
    (?P<port>:\d{1,5})?                  # optional port
    (?P<path>/[^\s?#]*)?                 # optional path
    (\?(?:[^#\s]*))?                     # optional query string
    (#.*)?$                              # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_path(input_path: str) -> bool:
    """
    Determine whether `input_path` is a valid HTTP/HTTPS URL.

    The function uses a regular expression that accepts the scheme
    (http or https), an optional port, and an optional path/query/fragment.
    It returns True if the entire string matches this pattern; otherwise False.

    Parameters
    ----------
    input_path : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the input is a valid HTTP/HTTPS URL, False otherwise.
    """
    # Reject empty strings immediately
    if not input_path:
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_URL_REGEX.fullmatch(input_path))