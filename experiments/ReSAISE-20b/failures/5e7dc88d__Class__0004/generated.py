import re
from urllib.parse import urlparse, urlunparse, urljoin

# Regular expression to detect a scheme (e.g. http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL to an absolute URL based on the
    request environment.

    Parameters:
        value (str): The location string to normalize.
        host_name (str): Hostname of the request (e.g. "example.com").
        url_scheme (str): Scheme of the request (e.g. "https").

    Returns:
        str: An absolute URL.

    Raises:
        ValueError: If the input value is not a valid URL or contains
                    unsafe components (e.g., leading '..').
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already contains a scheme, return it unchanged
    if SCHEME_RE.match(value):
        # Validate the URL structure to avoid malformed inputs
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid absolute URL: {value}")
        return value

    # Reject unsafe relative URLs that could traverse outside the intended
    # resource sphere (CWE-610 mitigation)
    if '..' in value.split('/'):
        raise ValueError("Relative URL contains unsafe path traversal")

    # Build the base URL from scheme and host
    base_url = f"{url_scheme}://{host_name}"
    # Ensure the base URL ends with a slash for proper joining
    if not base_url.endswith('/'):
        base_url += '/'

    # Join the relative path with the base URL
    absolute = urljoin(base_url, value)

    # Final validation to ensure we didn't produce an unexpected URL
    parsed_abs = urlparse(absolute)
    if not parsed_abs.scheme or not parsed_abs.netloc:
        raise ValueError(f"Failed to construct absolute URL from: {value}")

    return absolute