import re
from urllib.parse import urlparse, urljoin

# Regular expression to detect an existing scheme in a URL.
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+\-.]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL based on the request environment.

    Parameters
    ----------
    value : str
        The relative or absolute URL that needs to be made into an absolute path.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL combining the request's base URL and the provided value.

    Notes
    -----
    * If ``value`` already contains a scheme (detected via ``SCHEME_RE``), it is returned unchanged.
    * Otherwise, the function constructs a base URL from ``url_scheme`` and ``host_name`` and
      uses :func:`urllib.parse.urljoin` to resolve the relative path.
    """
    if not isinstance(value, str):
        raise TypeError(f"value must be a string, got {type(value).__name__}")

    if SCHEME_RE.match(value):
        # Already absolute, return as-is.
        return value

    base = f"{url_scheme}://{host_name}"
    # urljoin handles leading slashes, relative paths, and query strings.
    return urljoin(base, value)