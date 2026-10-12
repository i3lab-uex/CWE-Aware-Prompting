import re

# Regular expression for a valid http or https URL.
# It matches:
#   - scheme: http or https
#   - authority: hostname (with optional port)
#   - path, query and fragment are optional
# It is intentionally permissive with the host part but still rejects obvious
# malformed URLs. The regex is anchored to match the entire string.
_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                                 # http:// or https://
    (?:(?P<userinfo>[^:@/]+(?::[^@/]*)?)@)?                # optional userinfo
    (?P<host>
        \[?[A-Fa-f0-9:.]+\]?                              # IPv4, IPv6 or hostname
    )
    (?::(?P<port>\d{1,5}))?                                # optional port
    (?P<path>/[^\s?#]*)?                                   # optional path
    (?:\?(?P<query>[^\s#]*))?                              # optional query
    (?:\#(?P<fragment>.*))?                                # optional fragment
    $""",
    re.VERBOSE | re.IGNORECASE,
)

def validate_path(path: str) -> bool:
    """
    Validate that the given string is a syntactically correct http or https URL.

    Parameters
    ----------
    path : str
        The string to validate.

    Returns
    -------
    bool
        True if `path` matches the http/https URL pattern, False otherwise.
    """
    # Reject non-string inputs early to avoid unexpected errors.
    if not isinstance(path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _URL_RE.fullmatch(path.strip())
    return bool(match)