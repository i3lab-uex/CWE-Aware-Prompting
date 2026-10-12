import re
from urllib.parse import urljoin

# Regex to detect a scheme in a URL (e.g., "http:", "https:")
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute one using the
    provided host name and scheme.

    Parameters
    ----------
    value : str
        The URL to be converted. It may already contain a scheme.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL. If `value` already contains a scheme, it is returned unchanged.
        Otherwise the function prefixes the URL with the supplied scheme and host.

    Notes
    -----
    - The function assumes `value` is a valid URL path or full URL.
    - No explicit error handling for malformed URLs; any exception will propagate
      naturally from `urljoin`.
    """
    # If the value already contains a scheme, leave it untouched
    if SCHEME_RE.search(value):
        return value

    # Construct the base URL (scheme://host_name)
    base_url = f"{url_scheme.lower()}://{host_name}"
    # Join the base URL with the relative path
    absolute_url = urljoin(base_url, value)

    return absolute_url