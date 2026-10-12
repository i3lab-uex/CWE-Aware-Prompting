import re
from urllib.parse import urlparse, urljoin

# Regex to detect an absolute URL scheme (e.g., "http:", "https:")
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a location value into an absolute URL based on the request environment.

    Parameters
    ----------
    value : str
        The location string that may be relative or absolute.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL that can safely be used for redirects or location headers.

    Notes
    -----
    - If *value* already contains a scheme (e.g., "http://..."), it is returned unchanged.
    - If *value* starts with a slash or is a relative path, it will be joined to the base URL
      constructed from *url_scheme* and *host_name*.
    - The function is intentionally conservative to avoid CWE-601: it never redirects
      to an external host unless the input explicitly contains a scheme.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already has a scheme, treat it as absolute and return it unchanged.
    if SCHEME_RE.match(value):
        # Validate that the URL is parseable to avoid malformed redirects.
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid absolute URL: {value}")
        return value

    # Build the base URL from scheme and host.
    base = f"{url_scheme}://{host_name}"
    # urljoin handles leading slashes and relative paths correctly.
    absolute_url = urljoin(base, value)

    # Final sanity check: ensure the resulting URL is still under the same host.
    parsed = urlparse(absolute_url)
    if parsed.scheme != url_scheme or parsed.netloc != host_name:
        # This should never happen because we just constructed it, but guard anyway.
        raise ValueError("Constructed URL points to an unexpected host")

    return absolute_url