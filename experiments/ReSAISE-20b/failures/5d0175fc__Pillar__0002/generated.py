import re

# Compile the regex once at import time to avoid repeated compilation.
# The pattern matches a full HTTP or HTTPS URL with an optional port and path.
_HTTP_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme followed by ://
    (?:[a-zA-Z0-9\-._~%]+)              # hostname (simplified)
    (?::\d{1,5})?                       # optional port
    (?:/[^?#]*)?                        # optional path
    (?:\?[^\#]*)?                       # optional query string
    (?:\#[^\s]*)?                       # optional fragment
    $                                   # end of string
    """,
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify that the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches a valid http/https URL pattern, False otherwise.
    """
    # Guard against non-string input to avoid TypeError
    if not isinstance(address, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return _HTTP_URL_RE.fullmatch(address) is not None