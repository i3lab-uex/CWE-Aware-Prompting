import re
from urllib.parse import urlparse, urljoin

# Regex to detect a scheme at the start of the URL (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL based on the request
    environment.

    Parameters
    ----------
    value : str
        The URL to be converted. May be relative or absolute.
    host_name : str
        The hostname part of the request (e.g., 'example.com').
    url_scheme : str
        The scheme part of the request (e.g., 'https').

    Returns
    -------
    str
        An absolute URL that combines the scheme, host name and the provided value.

    Notes
    -----
    * If `value` already contains a scheme (checked by SCHEME_RE), it is returned
      unchanged.
    * Otherwise, the function constructs an absolute URL by prepending the scheme
      and host name to `value` using ``urllib.parse.urljoin`` for proper handling
      of slashes.
    """
    # If the value already has a scheme, assume it is absolute and return as-is
    if SCHEME_RE.match(value):
        return value

    # Build the base URL from scheme and host name
    base = f"{url_scheme}://{host_name}"
    # Use urljoin to correctly combine the base and relative path
    absolute_url = urljoin(base + '/', value)

    # Sanity check: ensure the result parses correctly
    parsed = urlparse(absolute_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Unable to construct absolute URL from value: {value}")

    return absolute_url