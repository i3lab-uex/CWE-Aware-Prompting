import re
from urllib.parse import urlparse, urljoin

# Regular expression to detect a URL scheme (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL to an absolute URL based on the request
    environment.

    Parameters:
        value (str): The user supplied location. It may be a relative path or
                     already an absolute URL.
        host_name (str): The hostname of the current request (e.g., 'example.com').
        url_scheme (str): The scheme used for the current request ('http' or 'https').

    Returns:
        str: An absolute URL. If `value` already contains a scheme, it is returned
             unchanged; otherwise the function prepends the request's base URL.

    Raises:
        ValueError: If any of the arguments are not valid strings or if the
                    constructed URL is malformed.
    """
    # Basic input validation
    if not isinstance(value, str) or not isinstance(host_name, str) or not isinstance(url_scheme, str):
        raise ValueError("All arguments must be strings")

    # If value already has a scheme, return it unchanged
    if SCHEME_RE.match(value):
        return value

    # Construct the base URL (scheme://host)
    base_url = f"{url_scheme}://{host_name}"
    # Use urljoin to correctly handle relative paths
    absolute_url = urljoin(base_url, value)

    # Basic sanity check: ensure the result is a valid absolute URL
    parsed = urlparse(absolute_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Resulting URL is invalid: {absolute_url}")

    return absolute_url