import re
from urllib.parse import urljoin

# Regular expression to detect a scheme at the beginning of a URL.
SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*:')

def make_location_absolute(value: str, host_name: str, url_scheme: str) -> str:
    """
    Convert a relative or absolute URL into an absolute URL based on the
    request environment.

    Parameters
    ----------
    value : str
        The URL to convert. May be relative, scheme‑relative (starting with '//'),
        or already absolute.
    host_name : str
        The hostname part of the request (e.g. 'example.com').
    url_scheme : str
        The scheme part of the request (e.g. 'https').

    Returns
    -------
    str
        An absolute URL that resolves the given value against the request base.

    Notes
    -----
    * If ``value`` already contains a scheme (e.g. 'http://...'), it is returned
      unchanged.
    * If ``value`` starts with '//', the scheme of the request is prefixed
      (scheme‑relative URLs).
    * Otherwise ``value`` is joined with the request's base URL.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    # If the value already has a scheme (e.g. 'http://'), return it unchanged.
    if SCHEME_RE.match(value):
        return value

    # If the value is scheme‑relative (starts with '//'), prepend the request
    # scheme to make it absolute.
    if value.startswith('//'):
        return f'{url_scheme}:{value}'

    # Ensure the base URL ends with a slash so that urljoin behaves as expected.
    base = f'{url_scheme}://{host_name}'
    # urljoin will correctly handle relative paths, query strings and fragments.
    return urljoin(base + '/', value)