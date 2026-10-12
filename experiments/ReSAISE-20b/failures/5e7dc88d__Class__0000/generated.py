import re
from urllib.parse import urlparse, urlunparse, urljoin

# Regex to detect if a URL already has a scheme (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a potentially relative URL into an absolute URL based on the request environment.

    Parameters
    ----------
    value : str
        The location string to be converted. It may already contain a scheme.
    host_name : str
        The hostname part of the request (e.g., "example.com").
    url_scheme : str
        The scheme part of the request (e.g., "https").

    Returns
    -------
    str
        An absolute URL string. If `value` already contains a scheme, it is returned unchanged.
        Otherwise, the function prepends the given scheme and hostname.

    Notes
    -----
    This implementation performs minimal validation to avoid unintentionally resolving
    URLs that point outside the intended domain. It only checks for an existing scheme
    and then uses :func:`urllib.parse.urljoin` to construct the absolute URL.
    """
    if not isinstance(value, str) or not isinstance(host_name, str) or not isinstance(url_scheme, str):
        raise TypeError("All arguments must be strings")

    # If the value already contains a scheme, return it unchanged
    if SCHEME_RE.match(value):
        return value

    # Construct the base URL from scheme and host_name
    base_url = f"{url_scheme.rstrip(':')}://{host_name.lstrip(':/')}"
    # Ensure base_url ends with a slash so that urljoin behaves correctly
    if not base_url.endswith('/'):
        base_url += '/'

    # Use urljoin to resolve the relative URL against the base
    absolute = urljoin(base_url, value)

    # Optional: Validate that the resulting URL is still within the same host
    parsed = urlparse(absolute)
    if parsed.hostname and parsed.hostname.lower() != host_name.lower():
        # This could be a redirection to an external domain; raise an error or handle as needed
        raise ValueError(f"Resulting URL points to a different host: {parsed.hostname}")

    return absolute