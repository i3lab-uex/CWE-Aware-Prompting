import re
from urllib.parse import urlparse, urlunparse

# Regular expression to detect a URL scheme (e.g. "http:" or "https:")
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL using the
    provided host name and scheme.

    Parameters
    ----------
    value : str
        The URL that may be relative or already absolute.
    host_name : str
        The hostname part of the request (e.g. "example.com").
    url_scheme : str
        The scheme part of the request (e.g. "https").

    Returns
    -------
    str
        An absolute URL that combines the request's base URL and the provided value.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already contains a scheme, return it unchanged.
    if SCHEME_RE.match(value):
        # Validate that the URL can be parsed; raise ValueError otherwise.
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid absolute URL: {value!r}")
        return value

    # Build a base URL from the scheme and host_name
    if not isinstance(host_name, str) or not host_name:
        raise ValueError("host_name must be a non-empty string")
    if not isinstance(url_scheme, str) or not url_scheme:
        raise ValueError("url_scheme must be a non-empty string")

    base = f"{url_scheme}://{host_name}"
    # Ensure the base ends with a slash for proper urljoin behavior
    if not base.endswith('/'):
        base += '/'

    # Use urlparse to join relative paths safely
    joined = urlparse(value)
    if joined.scheme or joined.netloc:
        # In case value contains a fragment or query but no scheme/netloc
        # We treat it as relative to the base.
        joined = joined._replace(scheme='', netloc='')

    absolute = urlparse(base)._replace(path=joined.path,
                                       params=joined.params,
                                       query=joined.query,
                                       fragment=joined.fragment)
    return urlunparse(absolute)

# Example usage:
if __name__ == "__main__":
    print(make_location_absolute("/login", "example.com", "https"))
    print(make_location_absolute("http://other.com/page", "example.com", "https"))