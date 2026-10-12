import re
from urllib.parse import urlparse, urljoin

# Regular expression that matches a scheme at the beginning of a URL
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+\-.]*:')  # e.g., http:, https:

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or scheme‑less URL into an absolute one based on the
    request's host and scheme.

    Parameters
    ----------
    value : str
        The location URL to be made absolute.  If it already contains a scheme,
        it is returned unchanged.
    host_name : str
        The hostname part of the request (e.g., "example.com").
    url_scheme : str
        The scheme part of the request (e.g., "https").

    Returns
    -------
    str
        An absolute URL that can be used for redirects or location headers.
    """
    # If the value already has a scheme, return it unchanged
    if SCHEME_RE.match(value):
        return value

    # Build the base URL from scheme and host
    # Ensure that we do not double‑add slashes
    base_url = f"{url_scheme.rstrip(':') or 'http'}://{host_name.lstrip('/')}"
    # urljoin handles relative paths correctly
    absolute_url = urljoin(base_url, value.lstrip('/'))

    # Basic validation: ensure we have a scheme and netloc
    parsed = urlparse(absolute_url)
    if not (parsed.scheme and parsed.netloc):
        raise ValueError(f"Invalid URL constructed: {absolute_url}")

    return absolute_url