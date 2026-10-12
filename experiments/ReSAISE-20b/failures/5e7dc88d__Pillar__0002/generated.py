import re
from urllib.parse import urlparse, urlunparse, urljoin

# Regular expression to detect a scheme in a URL (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL based on the request environment.

    Parameters
    ----------
    value : str
        The URL to be converted. If it already contains a scheme, it is returned unchanged.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL constructed from the request's base and the provided value.

    Notes
    -----
    * If `value` already contains a scheme (as detected by ``SCHEME_RE``), it is returned as-is.
    * Otherwise, the function constructs an absolute URL by joining the request's base
      (scheme + hostname) with `value`. Leading slashes in `value` are preserved.
    * The implementation uses ``urllib.parse.urljoin`` to correctly handle relative
      paths and query strings.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already contains a scheme, return it unchanged.
    if SCHEME_RE.match(value):
        return value

    # Build the base URL from scheme and host name.
    # Ensure the host_name does not contain a path or query part.
    base_netloc = host_name
    if ':' in host_name:
        # In case a port is included, keep it as part of netloc
        base_netloc = host_name

    # Construct the absolute URL.
    base_url = f"{url_scheme}://{base_netloc}"
    absolute_url = urljoin(base_url, value)

    # Validate the result to avoid malformed URLs.
    parsed = urlparse(absolute_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Unable to construct a valid absolute URL from '{value}'")

    return urlunparse(parsed)