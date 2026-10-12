import re
from urllib.parse import urlparse

# Regex to detect a scheme at the start of a URL (e.g., http:, https:)
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL using the
    provided host name and scheme.

    Parameters
    ----------
    value : str
        The URL to be made absolute. Can be relative (e.g., '/path') or
        already absolute (e.g., 'http://example.com').
    host_name : str
        The hostname of the current request (e.g., 'example.com').
    url_scheme : str
        The scheme of the current request (e.g., 'https').

    Returns
    -------
    str
        An absolute URL. If `value` already contains a scheme, it is returned unchanged.
    """
    # Strip leading/trailing whitespace
    value = value.strip()

    # If the URL already has a scheme, return it unchanged.
    if SCHEME_RE.match(value):
        return value

    # Ensure the path starts with a slash
    if not value.startswith('/'):
        value = '/' + value

    # Build the absolute URL
    return f'{url_scheme}://{host_name}{value}'