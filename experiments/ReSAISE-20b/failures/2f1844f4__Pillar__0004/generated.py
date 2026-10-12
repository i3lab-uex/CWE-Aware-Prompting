import re

# A reasonably strict pattern that matches a valid http or https URL.
# It ensures the scheme, host (with optional subdomains), optional port,
# and path/query/fragment components are present.  The pattern is
# deliberately simple to avoid catastrophic backtracking and to keep the
# function fast while still catching most malformed URLs.
_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                               # http or https scheme
    (?:(?P<user>[a-zA-Z0-9._%+-]+)(?:\:(?P<pwd>[^@]*))?@)?   # optional user:pwd@
    (?P<host>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})           # domain name
    (?::(?P<port>\d{1,5}))?                               # optional :port
    (?P<path>/[^?#]*)?                                    # path component
    (?:\?(?P<query>[^#]*))?                               # optional query string
    (?:\#(?P<fragment>.*))?$                              # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether *site_path* is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential URL.

    Returns
    -------
    bool
        ``True`` if *site_path* matches the URL pattern, otherwise ``False``.

    Notes
    -----
    - The function does not attempt to resolve the URL or check network
      connectivity; it only verifies that the syntax conforms to the pattern.
    - No exceptions are raised for invalid input; any unexpected errors
      during matching return ``False``.
    """
    try:
        # The match must cover the entire string; re.fullmatch is equivalent
        # to using ^...$ anchors in the pattern.
        return bool(_URL_RE.fullmatch(site_path))
    except Exception:
        # Any unforeseen error (e.g., regex compilation issue) is treated as
        # an invalid path to avoid leaking information.
        return False