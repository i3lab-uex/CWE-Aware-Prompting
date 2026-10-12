import re
from urllib.parse import urlparse, urljoin

# Regex that matches a scheme (e.g., "http:", "https:")
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL based on the
    request environment.

    Parameters:
        value (str): The location string to be made absolute.
        host_name (str): The hostname of the current request.
        url_scheme (str): The scheme ('http' or 'https') of the current request.

    Returns:
        str: An absolute URL that combines the base URL and the provided value.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already has a scheme, return it unchanged.
    if SCHEME_RE.match(value):
        return value

    # Build the base URL from scheme and host name.
    # Ensure there is no trailing slash on host_name to avoid double slashes.
    base_url = f"{url_scheme}://{host_name.rstrip('/')}/"

    # Use urljoin to correctly handle relative paths.
    absolute_url = urljoin(base_url, value.lstrip('/'))

    # Ensure the result is a valid absolute URL.
    parsed = urlparse(absolute_url)
    if not (parsed.scheme and parsed.netloc):
        raise ValueError(f"Unable to construct a valid absolute URL from {value}")

    return absolute_url