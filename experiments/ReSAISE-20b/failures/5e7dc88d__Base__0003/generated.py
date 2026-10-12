import re
from urllib.parse import urlparse, urljoin

# Regex to detect a scheme (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or scheme‑less URL into an absolute URL based on the
    request environment.

    Parameters
    ----------
    value : str
        The location string to be made absolute. It may already contain a scheme,
        or it may be relative.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL. If ``value`` already contains a scheme, it is returned
        unchanged; otherwise the function prefixes it with ``{url_scheme}://{host_name}``.

    Notes
    -----
    This helper does **not** perform any validation of whether the resulting URL
    is safe for redirection.  The caller should ensure that redirects are only
    sent to trusted destinations or otherwise validate the URL against a
    whitelist.

    Examples
    --------
    >>> make_location_absolute('/login', 'example.com', 'https')
    'https://example.com/login'
    >>> make_location_absolute('http://malicious.com', 'example.com', 'https')
    'http://malicious.com'
    """
    # Return unchanged if a scheme is already present
    if SCHEME_RE.match(value):
        return value

    # Ensure host_name and url_scheme are provided
    if not host_name or not url_scheme:
        raise ValueError("Both host_name and url_scheme must be provided")

    # Build the base URL
    base = f"{url_scheme}://{host_name}"
    # urljoin handles leading/trailing slashes correctly
    absolute = urljoin(base, value)

    # Normalise the result to avoid double slashes
    parsed = urlparse(absolute)
    normalized = parsed._replace(path=parsed.path or "/")
    return normalized.geturl()