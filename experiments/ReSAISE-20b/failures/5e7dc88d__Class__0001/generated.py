import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Regex to detect a scheme at the beginning of a URL (e.g. "http:" or "https:")
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute one based on the
    request environment.

    Parameters
    ----------
    value : str
        The URL that may be relative or already absolute.
    host_name : str
        The hostname of the current request (e.g., "example.com").
    url_scheme : str
        The scheme of the current request (e.g., "https").

    Returns
    -------
    str
        An absolute URL that combines the scheme, host and provided path.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already contains a scheme, return it unchanged
    if SCHEME_RE.match(value):
        # Ensure the URL is parsed correctly to avoid malformed URLs
        parsed = urlparse(value)
        return urlunparse(parsed)

    # Build a base URL from the scheme and host
    base = f"{url_scheme}://{host_name}"
    # Join the relative path with the base URL
    joined = urlparse(urljoin(base, value))
    return urlunparse(joined)

# Helper function for joining URLs
def urljoin(base: str, rel: str) -> str:
    """
    Join a base URL with a relative path. This function ensures that the
    resulting URL is properly constructed even if `rel` starts with a slash.
    """
    base_parsed = urlparse(base)
    # If rel is an absolute path, strip leading slash to avoid double slashes
    if rel.startswith('/'):
        rel = rel[1:]
    joined_path = f"{base_parsed.path.rstrip('/')}/{rel}"
    return urlunparse(ParseResult(
        scheme=base_parsed.scheme,
        netloc=base_parsed.netloc,
        path=joined_path,
        params='',
        query='',
        fragment=''
    ))