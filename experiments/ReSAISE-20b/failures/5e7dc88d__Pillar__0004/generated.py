import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Regular expression that matches a scheme at the beginning of a URL (e.g. http:, https:)
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute location into an absolute URL.

    Parameters
    ----------
    value : str
        The location to be converted.  If it already contains a scheme,
        the value is returned unchanged.
    host_name : str
        The hostname of the current request (e.g. "example.com").
    url_scheme : str
        The scheme of the current request (e.g. "https").

    Returns
    -------
    str
        An absolute URL combining the request's base URL and ``value``.

    Notes
    -----
    - If ``value`` already contains a scheme (e.g. "http://foo") it is returned as-is.
    - If ``value`` is relative (e.g. "/foo") it will be joined with the
      base URL constructed from ``url_scheme`` and ``host_name``.
    - The function does not perform any security checks on the resulting URL
      beyond basic scheme detection.  Callers should validate the final
      URL if needed.
    """
    # If a scheme is already present, return unchanged
    if SCHEME_RE.match(value):
        return value

    # Construct the base URL from scheme and host name
    base = f"{url_scheme}://{host_name}"
    # Ensure the base ends with a slash so that urljoin behaves correctly
    if not base.endswith('/'):
        base += '/'

    # Join the relative path with the base
    absolute = urlparse(urljoin(base, value))
    # Reconstruct a clean URL string
    return urlunparse(absolute)

# Helper function for joining URLs that mimics urllib.parse.urljoin but
# ensures we do not lose fragments or query strings in the relative part.
def urljoin(base: str, rel: str) -> str:
    """
    Join a base URL and a relative URL.  This helper is used by
    ``make_location_absolute`` to avoid side effects from the standard
    library's implementation when dealing with edge cases.
    """
    parsed_base = urlparse(base)
    if rel.startswith('//'):
        # Network-path reference: keep the scheme from base
        return f"{parsed_base.scheme}:{rel}"
    if rel.startswith('/'):
        # Absolute path relative to the host
        return f"{parsed_base.scheme}://{parsed_base.netloc}{rel}"
    # Relative path: join with the base's path
    new_path = parsed_base.path.rsplit('/', 1)[0] + '/' + rel
    return f"{parsed_base.scheme}://{parsed_base.netloc}{new_path}"