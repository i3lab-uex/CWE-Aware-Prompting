import re
from urllib.parse import urljoin

# Regex to detect if a URL has an explicit scheme (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or scheme‑less URL into an absolute URL based on the request's
    host and scheme.

    Parameters
    ----------
    value : str
        The location string that may be relative, scheme‑less, or already absolute.
    host_name : str
        The hostname (or hostname:port) of the current request.
    url_scheme : str
        The scheme used by the request (e.g., 'http' or 'https').

    Returns
    -------
    str
        An absolute URL that combines the request's base URL with `value`.

    Notes
    -----
    - If `value` already contains a scheme, it is returned unchanged.
    - The function uses :func:`urllib.parse.urljoin` to safely combine URLs,
      which handles leading slashes and relative paths correctly.
    """
    # If the value already contains a scheme, return it unchanged
    if SCHEME_RE.match(value):
        return value

    # Build the base URL from scheme and host
    base_url = f"{url_scheme}://{host_name}"
    # Use urljoin to combine the base with the relative value
    absolute_url = urljoin(base_url, value)

    return absolute_url