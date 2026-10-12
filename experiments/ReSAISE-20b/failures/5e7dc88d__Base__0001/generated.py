import re
from urllib.parse import urlparse, urlunparse

# Regular expression that matches a URL scheme (e.g. "http:" or "https:")
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or scheme-less URL to an absolute one based on the
    request's host and scheme.

    Parameters
    ----------
    value : str
        The URL to be converted. It may be absolute, relative or missing a scheme.
    host_name : str
        The hostname of the current request (e.g. "example.com").
    url_scheme : str
        The scheme of the current request (e.g. "https").

    Returns
    -------
    str
        An absolute URL that can safely be used in redirects or location headers.

    Notes
    -----
    * If `value` already contains a scheme, it is returned unchanged.
    * If the value is relative (e.g. "/path" or "page.html"), it will be
      prefixed with the supplied scheme and host.
    * The function performs minimal validation; callers should ensure
      `host_name` is trustworthy to avoid open‑redirect vulnerabilities.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already has a scheme (e.g., "http://...") we trust it
    # and return it unchanged.
    if SCHEME_RE.search(value):
        return value

    # Ensure the path starts with a slash so that urlunparse produces
    # an absolute URL.
    path = value if value.startswith("/") else f"/{value}"

    # Construct a new URL using the supplied scheme and host.
    absolute_parts = (url_scheme, host_name, path, "", "", "")
    return urlunparse(absolute_parts)