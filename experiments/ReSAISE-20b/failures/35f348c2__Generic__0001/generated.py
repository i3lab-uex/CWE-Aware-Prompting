import re

# Regular expression that validates an HTTP or HTTPS URL.
# It checks for the scheme, a domain (or IPv6 address in brackets),
# an optional port number, and an optional path/query/fragment.
_URL_REGEX = re.compile(
    r'''
    ^                                   # start of string
    https?://                           # http:// or https://
    (?:                                 # host part
        [A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?   # hostname label
        (?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?)*  # more labels
        |                               # or IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |                               # or IPv6 in brackets
        \[ [A-Fa-f0-9:]+ \]
    )
    (?: :\d{1,5} )?                    # optional port
    (?: /[^\\s]* )?                     # optional path/query/fragment
    $                                   # end of string
    ''',
    re.VERBOSE | re.IGNORECASE
)

def validate_path(path: str) -> bool:
    """
    Validate whether the given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if `path` matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Ensure we get a string and not None
    if not isinstance(path, str):
        return False

    # Use fullmatch to ensure the entire string matches the pattern
    return bool(_URL_REGEX.fullmatch(path))