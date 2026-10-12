import re

# Compile the regex once at import time to avoid repeated compilation.
# This pattern matches URLs that start with http:// or https://, followed by
# a valid hostname (letters, digits, hyphens, dots), an optional port,
# and an optional path/query/fragment. It is intentionally permissive
# while rejecting obvious invalid inputs such as missing scheme or
# unsupported characters.
_URL_RE = re.compile(
    r'''
    ^                                   # start of string
    (https?)://                         # http or https scheme with ://
    (?:
        [a-zA-Z0-9]                     # first hostname char
        (?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?  # middle hostname part
        (?:\.[a-zA-Z]{2,})+            # one or more dot-separated TLDs
    )
    (?::\d{1,5})?                       # optional port (0-65535)
    (?:/[^\s?#]*)?                      # optional path, no spaces
    (?:\?[^\s#]*)?                      # optional query string, no spaces
    (?:#[^\s]*)?                        # optional fragment, no spaces
    $                                   # end of string
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def validate_path(path: str) -> bool:
    """
    Validate whether the input string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.

    Notes
    -----
    The function never raises an exception. It simply returns False for any
    input that does not conform to the pattern.
    """
    if not isinstance(path, str):
        return False
    # Using fullmatch ensures the entire string matches the pattern.
    return bool(_URL_RE.fullmatch(path))