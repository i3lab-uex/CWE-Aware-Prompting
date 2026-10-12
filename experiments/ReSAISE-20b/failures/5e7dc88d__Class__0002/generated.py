import re
from urllib.parse import urljoin

# Regex to detect a URL scheme (e.g. http:, https:, ftp:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL to an absolute URL based on the request's
    scheme and host.

    Parameters:
        value (str): The location value that may be relative or absolute.
        host_name (str): Hostname of the current request (e.g., "example.com").
        url_scheme (str): Scheme of the current request (e.g., "https").

    Returns:
        str: An absolute URL.

    Notes:
        - If `value` already contains a scheme, it is returned unchanged.
        - Otherwise, the function constructs an absolute URL by joining
          `value` to the base URL formed from `url_scheme` and `host_name`.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if SCHEME_RE.match(value):
        # Already absolute, return as is
        return value

    # Construct the base URL; ensure it ends with a slash for correct joining
    base = f"{url_scheme}://{host_name}"
    if not base.endswith('/'):
        base += '/'

    # Use urljoin to handle relative paths correctly
    absolute_url = urljoin(base, value)
    return absolute_url