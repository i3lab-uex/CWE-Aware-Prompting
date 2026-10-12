import re

# Regular expression to validate a full HTTP or HTTPS URL.
# It checks for:
#   - http:// or https:// scheme
#   - a non-empty hostname (letters, digits, hyphen, dot)
#   - optional port number
#   - optional path/query fragment that does not contain whitespace
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme
    (?P<host>[a-zA-Z0-9.-]+)            # hostname (letters, digits, dots, hyphens)
    (?::(?P<port>\d{1,5}))?             # optional :port
    (?P<path>/[^\s?#]*                    # path starting with /
        (?:\?[^\s#]*)?                   # optional query string
        (?:#[^\s]*)?                     # optional fragment
    )?$                                  # end of string
    """,
    re.VERBOSE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Return True if `site_path` is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.

    Parameters
    ----------
    site_path : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the input matches the expected HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    - No exceptions are raised; invalid input simply returns False.
    - The regex is intentionally simple and avoids back‑tracking pitfalls
      by using explicit character classes and limiting repetitions.
    """
    if not isinstance(site_path, str):
        return False
    return _URL_RE.match(site_path) is not None