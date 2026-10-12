import re
from urllib.parse import urljoin, urlparse

# Regular expression that matches a scheme at the start of a URL
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*:')


def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute location URL into an absolute URL based on the
    current request environment.

    Parameters
    ----------
    value : str
        The location string that may be relative (e.g. '/login') or absolute
        (e.g. 'http://example.com/login').
    host_name : str
        The hostname of the current request (e.g. 'example.com').
    url_scheme : str
        The scheme of the current request (e.g. 'https').

    Returns
    -------
    str
        An absolute URL constructed from the provided values. If `value`
        already contains a scheme, it is returned unchanged.

    Notes
    -----
    * If `value` starts with a slash, it is considered an absolute path on
      the current host.
    * If `value` does not start with a slash, it is treated as a relative
      path and joined to the host root.
    * The function does not attempt to resolve network paths or validate
      that the resulting URL is reachable.
    """
    # If value already contains a scheme, return it unchanged
    if SCHEME_RE.match(value):
        return value

    # Ensure host_name does not contain a scheme or trailing slash
    cleaned_host = host_name.strip().rstrip('/')

    # Build the base URL from scheme and hostname
    base_url = f"{url_scheme}://{cleaned_host}"

    # Use urljoin to combine the base URL with the provided value
    absolute_url = urljoin(base_url, value)

    # Sanity check: the result should be a valid absolute URL
    parsed = urlparse(absolute_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Failed to construct a valid absolute URL from '{value}'")

    return absolute_url